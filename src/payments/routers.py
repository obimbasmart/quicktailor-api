
from fastapi import APIRouter, Depends, Request, HTTPException, status
from src.payments.schemas import PaystackWebhookPayload
from src.auth.dependencies import get_current_user
from src.payments.schemas import CheckOut
from src.payments.CRUD import create_payment
from src.payments.dependencies import initiate_payment, verify_paystack_signature
from src.orders.models import Order
from src.orders.CRUD import create_orders
from dependencies import get_db
from pprint import pprint as pp

router = APIRouter(
    tags=["payment", "order"],
)


@router.post("/webhooks/paystack")
async def paystack_webhook(request: Request,
                           db=Depends(get_db),
                           verified=Depends(verify_paystack_signature)):

    payload: PaystackWebhookPayload = await request.json()
    if payload.get('event') == "charge.success":
        payment_data = payload.get('data')
        payment = create_payment(payment_data, db)
        orders = create_orders(cart=payment_data.get('metadata').get('cart'),
                               payment_id=payment.id,
                               db=db)


@router.post("/checkout")
async def checkout(req_body: CheckOut,
                   current_user=Depends(get_current_user),
                   payload=Depends(initiate_payment)):

    return payload