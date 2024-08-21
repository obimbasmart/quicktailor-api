from fastapi import APIRouter, Depends, File, UploadFile, Form
from fastapi.responses import JSONResponse
from src.auth.dependencies import get_current_user
from src.tailors.CRUD import get_tailors, _update_tailor, _upload_verification_details
from src.tailors.dependencies import get_tailor_by_id, get_current_tailor
from src.orders.dependencies import get_order_by_id
from src.tailors.schemas import TailorItem, TailorListItem, UpdateTailor, VerificationInfo
from src.orders.schemas import TailorOrderListItem, TailorOrderItem
from src.reviews.schemas import ReviewItem
from dependencies import get_db
from typing import List
from pydantic import UUID4
from utils import verify_resource_access
from responses import update_success_response
from exceptions import unauthorized_access_exception


router = APIRouter(
    prefix="/tailors",
    tags=["tailors"],
)


@router.get('', response_model=List[TailorListItem])
def get_all_tailors(current_user=Depends(get_current_user),
                    db=Depends(get_db)):
    tailors = get_tailors(db)
    return tailors


@router.get('/{tailor_id}', response_model=TailorItem)
def get_single_tailor(tailor_id: UUID4,
                      current_user=Depends(get_current_user),
                      tailor=Depends(get_tailor_by_id)):
    return tailor


@router.put('/{tailor_id}', response_model=None)
def update_tailor(tailor_id: str,
                  req_body: UpdateTailor,
                  current_user=Depends(get_current_tailor),
                  db=Depends(get_db),
                  tailor=Depends(get_tailor_by_id)):

    verify_resource_access(tailor_id, current_user.id)
    tailor = _update_tailor(tailor, req_body, db)
    return update_success_response("Tailor")


@router.get('/{tailor_id}/reviews', response_model=List[ReviewItem])
def get_tailor_reviews(tailor_id: UUID4,
                       current_user=Depends(get_current_user),
                       tailor=Depends(get_tailor_by_id)):

    return tailor.reviews


@router.post('/{tailor_id}/verification')
def upload_verification_details(tailor_id: UUID4,
                                details: VerificationInfo,
                                current_user=Depends(get_current_tailor),
                                db=Depends(get_db),
                                tailor=Depends(get_tailor_by_id)):

    verify_resource_access(tailor.id, current_user.id)
    tailor = _upload_verification_details(tailor, details, db)
    return update_success_response('Verification details')


@router.get('/{tailor_id}/orders', response_model=List[TailorOrderListItem])
def get_tailor_orders(tailor_id: str,
                      current_user=Depends(get_current_tailor),
                      tailor=Depends(get_tailor_by_id)):
    verify_resource_access(tailor.id, current_user.id)
    return current_user.orders


@router.get('/{tailor_id}/orders/{order_id}', response_model=TailorOrderItem)
def get_tailor_orders(tailor_id: str,
                      order_id: str,
                      current_user=Depends(get_current_tailor),
                      tailor=Depends(get_tailor_by_id),
                      order=Depends(get_order_by_id)):
    verify_resource_access(tailor.id, current_user.id)

    if order.id not in [item.id for item in tailor.orders]:
        raise unauthorized_access_exception()

    return order
