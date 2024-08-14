from typing import Dict
from src.payments.models import Payment
from sqlalchemy.orm import Session
from datetime import datetime


def create_payment(payload: Dict, db: Session) -> Payment:
    payment = Payment(
        transaction_id=payload['id'],
        reference=payload['reference'],
        amount=payload['amount'],
        status=payload['status'],
        paid_at=datetime.strptime(payload['paidAt'], "%Y-%m-%dT%H:%M:%S.%fZ"),
        channel=payload['channel'],
        currency=payload['currency'],
        customer_email=payload['customer']['email'],
        customer_lastname=payload['customer']['first_name'],
        customer_firstname=payload['customer']['last_name'],
        meta_data=payload['metadata'],
    )

    db.add(payment)
    db.commit()
    db.refresh(payment)
    return payment
