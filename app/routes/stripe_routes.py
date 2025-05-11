# app/routes/stripe_routes.py
from fastapi import APIRouter, Depends, HTTPException
from ..firebase_auth import verify_firebase_token
import stripe
import os
from pydantic import BaseModel

router = APIRouter(prefix="/api/stripe")

stripe.api_key = os.getenv("STRIPE_SECRET_KEY")

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
            success_url="http://localhost:5173/profile?paid=1",
            cancel_url="http://localhost:5173/profile?cancelled=1",
            customer_email=email,
            metadata={"firebase_uid": uid}
        )
        return {"checkout_url": session.url}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
