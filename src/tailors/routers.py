from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from src.auth.dependencies import get_current_user
from src.tailors.CRUD import get_tailors
from src.tailors.dependencies import get_tailor_by_id
from src.tailors.schemas import TailorItem, TailorListItem
from dependencies import get_db
from typing import List
from pydantic import UUID4


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
def get_single_tailor(tailor_id: UUID4, current_user=Depends(get_current_user),
                      db=Depends(get_db), tailor=Depends(get_tailor_by_id)):
    return tailor


@router.get('/{tailor_id}/reviews', response_model=None)
def get_tailor_reviews(tailor_id: UUID4, current_user=Depends(get_current_user),
                      db=Depends(get_db), tailor=Depends(get_tailor_by_id)):
    return JSONResponse(status_code=200, content=[])
