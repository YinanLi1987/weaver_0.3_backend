# app/routes/stripe_webhook.py

from fastapi import APIRouter, Request, HTTPException
from app.db import SessionLocal
from app.models.user import User
import stripe
import os
from dotenv import load_dotenv
router = APIRouter(prefix="/api/stripe")
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

    if event["type"] == "checkout.session.completed":
        session = event["data"]["object"]
        uid = session["metadata"].get("firebase_uid")

        # Update balance in database
        db = SessionLocal()
        user = db.query(User).filter(User.uid == uid).first()
        if user:
            user.balance += 5.00  # You can also pass amount dynamically
            db.commit()
        db.close()

    return {"status": "success"}
