# app/routes/stripe_webhook.py

from fastapi import APIRouter, Request, HTTPException
from decimal import Decimal
from sqlalchemy.orm import Session
from app.db import SessionLocal
from app.models.user import User
from app.crud.payment import log_payment
from app.crud.user import update_user_balance
import stripe
import os
from dotenv import load_dotenv
router = APIRouter()
if os.getenv("HEROKU") is None:
    load_dotenv(dotenv_path=".env")
stripe.api_key = os.getenv("STRIPE_SECRET_KEY")
webhook_secret = os.getenv("STRIPE_WEBHOOK_SECRET")
if not stripe.api_key:
    raise RuntimeError("❌ Missing STRIPE_SECRET_KEY")

if not webhook_secret:
    raise RuntimeError("❌ Missing STRIPE_WEBHOOK_SECRET")

@router.post("/webhook")
async def stripe_webhook(request: Request):
    payload = await request.body()
    sig_header = request.headers.get("stripe-signature")

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, webhook_secret
        )
    except stripe.error.SignatureVerificationError:
        raise HTTPException(status_code=400, detail="Invalid Stripe signature")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Webhook error: {str(e)}")
    if event["type"] != "checkout.session.completed":
        return {"status": "ignored"}

    
    session_data = event["data"]["object"]
    uid = session_data["metadata"].get("firebase_uid")
    session_id = session_data["id"]
    amount_cents = session_data.get("amount_total", 0)
    currency = session_data.get("currency", "eur")
    db: Session = SessionLocal()

    try:
        user = db.query(User).filter(User.uid == uid).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        amount_decimal = Decimal(amount_cents) / 100  # Stripe uses cents

            # 记录付款日志
        log_payment(
                db=db,
                user_id=user.uid,
                amount=amount_decimal,
                stripe_session_id=session_id,
                currency=currency
            )

            # 更新用户余额
        update_user_balance(db, user_id=user.uid, delta=amount_decimal)

        return {"status": "success"}

    except Exception as e:
          db.rollback()
          raise HTTPException(status_code=500, detail=f"Webhook processing failed: {str(e)}")

    finally:
            db.close()
