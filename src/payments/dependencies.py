from src.payments.config import settings
import requests
from src.payments.schemas import CheckOut
from fastapi import status, HTTPException
from src.orders.CRUD import get_actual_money_paid, get_cart_items_by_id
from src.users.models import User
from src.payments.schemas import InitPayment
from sqlalchemy.orm import Session
from utils import generate_uuid
from fastapi import Request
import hmac
import hashlib
from src.payments.config import settings
from exceptions import not_found_exception, unauthorized_access_exception, access_denied_exception


async def verify_paystack_signature(request: Request) -> bool:
    paystack_signature = request.headers.get("x-paystack-signature")

    if not paystack_signature:
        raise unauthorized_access_exception(msg='Signature missing')

    generated_signature = hmac.new(
        settings.TEST_PUBLIC_KEY.encode('utf-8'),
        await request.body(),
        hashlib.sha512
    ).hexdigest()

    if hmac.compare_digest(generated_signature, paystack_signature):
        return True

    raise access_denied_exception(msg="Invalid signature")


def initiate_payment(user: User, req_body: CheckOut, db: Session):

    cart_items = get_cart_items_by_id(req_body.cart, db)

    if not cart_items or not all([item.user.id == user.id for item in cart_items]):
        raise not_found_exception

    amount = sum([
        get_actual_money_paid(item.id, item.product.price, db)
        for item in cart_items
    ]) * 100

    reference = generate_uuid()
    metadata = {
        "cart": req_body.cart,
        "user_id": user.id
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
