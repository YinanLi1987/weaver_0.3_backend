# app/routes/stripe_routes.py
from fastapi import APIRouter, Depends, HTTPException
from ..firebase_auth import verify_firebase_token
import stripe
import os
from pydantic import BaseModel
from dotenv import load_dotenv
router = APIRouter()
if os.getenv("HEROKU") is None:
    load_dotenv(dotenv_path=".env")
stripe.api_key = os.getenv("STRIPE_SECRET_KEY")
stripe_price_id = os.getenv("STRIPE_PRICE_ID")
frontend_url = os.getenv("FRONTEND_URL", "http://localhost:5173")

if stripe.api_key is None:
    raise Exception("Missing STRIPE_SECRET_KEY")
if not stripe.api_key:
    raise RuntimeError("❌ Missing STRIPE_SECRET_KEY")
if not stripe_price_id:
    raise RuntimeError("❌ Missing STRIPE_PRICE_ID")

class CheckoutResponse(BaseModel):
    checkout_url: str
@router.post("/checkout", response_model=CheckoutResponse)
def create_checkout(uid_email=Depends(verify_firebase_token)):
    uid, email = uid_email

    try:
        session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            mode="payment",
            line_items=[{
                "price": os.getenv("STRIPE_PRICE_ID"),  # from your product in Stripe
                "quantity": 1,
            }],
            success_url=f"{frontend_url}/profile?paid=1",
            cancel_url=f"{frontend_url}/profile?cancelled=1",
            customer_email=email,
            metadata={"firebase_uid": uid}
        )
        return {"checkout_url": session.url}
    except stripe.error.StripeError as e:
        raise HTTPException(status_code=502, detail=f"Stripe error: {e.user_message or str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal error: {str(e)}")
