from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from src.auth.dependencies import get_current_user
from src.tailors.CRUD import get_tailors
from src.tailors.dependencies import get_tailor_by_id, get_current_tailor
from src.tailors.schemas import TailorItem, TailorListItem, UpdateTailor
from dependencies import get_db
from typing import List
from pydantic import UUID4
from fastapi import HTTPException


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
    print(current_user.id)
    return tailor


@router.put('/{tailor_id}', response_model=None)
def get_tailor_reviews(tailor_id: UUID4,
                       req_body: UpdateTailor,
                       current_user=Depends(get_current_tailor),
                       db=Depends(get_db),
                       tailor=Depends(get_tailor_by_id)):
    
    if not tailor:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='Tailor not found')
    
    if tailor.id != current_user.id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='Access denied')


    update_data = req_body.model_dump(exclude_unset=True)
    
    [
        setattr(tailor, attr, value)
        for attr, value in update_data.items()
        if attr not in ['first_name', 'last_name']
    ]

    if not tailor.is_verified:
        [
            setattr(tailor, attr, value)
            for attr, value in update_data.items()
            if attr in ['first_name', 'last_name']
        ]

    db.commit()
    db.refresh(tailor)
    return JSONResponse(status_code=status.HTTP_200_OK,
                        content={"message": "Update successfull"})


@router.get('/{tailor_id}/reviews', response_model=None)
def get_tailor_reviews(tailor_id: UUID4, current_user=Depends(get_current_user),
                       db=Depends(get_db), tailor=Depends(get_tailor_by_id)):
    return JSONResponse(status_code=200, content=[])
