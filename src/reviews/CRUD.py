from sqlalchemy.orm import Session
from src.reviews.schemas import UploadReview
from src.reviews.models import Review

def create_new_review(review_data: UploadReview, user_id: str, order_id: str,  db: Session):
    
    check_review =  db.query(Review).filter(order_id==Review.order_id).one_or_none()
    if check_review:
        return None

    new_review = Review(**review_data.model_dump(), user_id = user_id, order_id = order_id)
    
    db.add(new_review)
    db.commit()
    db.refresh(new_review)
    return new_review