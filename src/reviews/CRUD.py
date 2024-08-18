from sqlalchemy.orm import Session
from src.reviews.schemas import UploadReview
from src.reviews.models import Review
from src.orders.models import Order
from src.tailors.models import Tailor
from src.users.models import User
from exceptions import already_exists_exception


def create_new_review(user: User, order: Order, req_body: UploadReview, db: Session):
    
    if get_review_by_order_id(order.id, db):
        raise already_exists_exception('Review')


    new_review = Review(**req_body.model_dump(),
                        user_id = user.id,
                        order_id = order.id)
    
    db.add(new_review)
    db.commit()
    db.refresh(new_review)
    return new_review

def get_tailor_reviews(tailor_id: str, db: Session):
    return db.query(Review) \
            .join(Review.order) \
            .join(Order.tailor) \
            .filter(Tailor.id == tailor_id)


def get_review_by_order_id(order_id: str, db: Session):
    return db.query(Review).filter(order_id==Review.order_id).one_or_none()