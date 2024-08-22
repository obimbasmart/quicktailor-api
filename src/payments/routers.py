
from fastapi import APIRouter, Depends, Request
from src.payments.schemas import PaystackWebhookPayload
from src.auth.dependencies import get_current_user
from src.payments.schemas import CheckOut
from src.payments.CRUD import create_payment
from src.payments.dependencies import initiate_payment, verify_paystack_signature
from src.orders.CRUD import create_orders
from dependencies import get_db
from src.carts.CRUD import clear_items_in_cart

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

        cart = payment_data.get('metadata').get('cart')

        create_orders(cart=cart,
                      payment_id=payment.id,
                      db=db)

        clear_items_in_cart(cart, db)


@router.post("/checkout")
async def checkout(req_body: CheckOut,
                   db=Depends(get_db),
                   current_user=Depends(get_current_user)):

    payload = initiate_payment(current_user, req_body, db)
    return payload
