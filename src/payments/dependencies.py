from src.payments.config import settings
import requests
from src.payments.schemas import CheckOut
from fastapi import status, HTTPException
from src.orders.CRUD import get_actual_money_paid, get_cart_items_by_id
from src.admin.CRUD import _get_user
from typing import List
from src.payments.schemas import InitPayment, PaystackWebhookPayload
from fastapi import Depends
from dependencies import get_db
from sqlalchemy.orm import Session
from utils import generate_uuid
from fastapi import Request
import hmac
import hashlib
from src.payments.config import settings


async def verify_paystack_signature(request: Request) -> bool:
    paystack_signature = request.headers.get("x-paystack-signature")

    if not paystack_signature:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Signature missing")

    generated_signature = hmac.new(
        settings.TEST_PUBLIC_KEY.encode('utf-8'),
        await request.body(),
        hashlib.sha512
    ).hexdigest()

    if hmac.compare_digest(generated_signature, paystack_signature):
        return True

    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN, detail="Invalid signature")



async def initiate_payment(req_body: CheckOut,
                     db: Session = Depends(get_db)):
    user = _get_user(req_body.user_id, db)

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="User not found")

    cart_items = get_cart_items_by_id(req_body.cart, db)

    if not cart_items or not all([item.user.id == user.id for item in cart_items]):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="One or more items not in cart")

    amount = sum([
        get_actual_money_paid(item.id, item.product.price, db)
        for item in cart_items
    ]) * 100

    reference = generate_uuid()
    metadata = {
        "cart": req_body.cart,
        "user_id": req_body.user_id
    }

    response = paystack_initiate_payment(
        InitPayment(amount=amount,
                    email=user.email,
                    reference=reference,
                    metadata=metadata)
    )

    if response.status_code != status.HTTP_200_OK:
        raise HTTPException(status_code=response.status_code,
                            detail=response.json())

    return response.json()


def paystack_initiate_payment(data: InitPayment):
    headers = {'Authorization': f'Bearer {settings.TEST_PUBLIC_KEY}'}
    return requests.post(url=settings.BASE_URL.format(suffix='/initialize'),
                         headers=headers, data=data.model_dump_json())


def generate_reference(cart: List[str]) -> str:
    return '-'.join(str(item.id)[-6:] for item in cart)
