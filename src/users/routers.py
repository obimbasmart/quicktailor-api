from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.responses import JSONResponse
from src.users.CRUD import get_users, update_user, update_measurement, add_favorite
from src.users.dependencies import get_user_by_id, get_current_user
from src.users.schemas import (UserInfo, AddFavorite,  UpdateFields, FavoriteResponse, 
        SuccessMsg, FemaleMeasurementInfo,  MaleMeasurementInfo, MeasurementUpdate)
from dependencies import get_db
from typing import List, Union
from pydantic import UUID4, ValidationError
from src.users.utils import get_user_via_email, get_products, get_tailors
from src.tailors.dependencies import get_tailor_by_id
from src.users.constants import MEASUREMENT_TYPES
from src.products.schemas import ProductItem
from src.products.models.product import Product
from src.products.CRUD import _get_product

router = APIRouter(
    prefix="/users",
    tags=["users"],
)

@router.get('', response_model=List[UserInfo])
async def get_all_users(current_user=Depends(get_current_user),
                    db=Depends(get_db)):
    users = get_users(db)
    return users

@router.get('/{user_id}', response_model=UserInfo)
async def get_single_user(user_id: UUID4, current_user=Depends(get_current_user),
                      db=Depends(get_db), user=Depends(get_user_by_id)):
    if not user:
        raise HTTPException(status_code=404, detail="User not found with the id")
    return user


@router.put('/{user_id}', response_model=SuccessMsg)
async def update_user_route(req_body: UpdateFields,  user_id: str, current_user=Depends(get_current_user),
                      db=Depends(get_db), user = Depends(get_user_by_id)):
    verify_email = get_user_via_email(req_body.email, db)
    if current_user.email == req_body.email:
        raise HTTPException(status_code=422, detail="This is your present Email")
    if verify_email:
        raise HTTPException(status_code=422, detail="Email is Already in use")
    print("request body",verify_email)
    if not user:
        raise HTTPException(status_code=404, detail="User not found with the id")
    if current_user.id != user_id:
        raise HTTPException(status_code=401, detail="Unauthorized request")

    update = update_user(user_id, req_body, db)
    return update

@router.get('/measurement/{user_id}', response_model=List[Union[MaleMeasurementInfo, FemaleMeasurementInfo]])
async def get_user_measurement(user_id: UUID4, current_user=Depends(get_current_user),
                      db=Depends(get_db), user=Depends(get_user_by_id)):
    if not user:
        raise HTTPException(status_code=404, detail="User not found with the id")
    formatted_measurements = []
    for measurement in user.measurement:
        if "measurement_type" in measurement and measurement['measurement_type'] == "MALE":    
            formatted_measurements.append(MaleMeasurementInfo(**measurement))
        else:
            formatted_measurements.append(FemaleMeasurementInfo(**measurement))

    return formatted_measurements

@router.put('/measurement/{user_id}', response_model=Union[MaleMeasurementInfo, FemaleMeasurementInfo])
async def update_user_measurement(req_body: MeasurementUpdate,
                            user_id: str, 
                            current_user=Depends(get_current_user),
                            db=Depends(get_db), user=Depends(get_user_by_id)):
    if user_id != current_user.id:
        raise HTTPException(status_code=401, detail="Unauthorized request")
    if not user:
        raise HTTPException(status_code=404, detail="User not found with the id")
    update = update_measurement(user_id, req_body, db)
    update = update_measurement(user_id, req_body, db)
    if update:
        if update['measurement_type'] == "MALE":   
             return MaleMeasurementInfo(**update)
        else:
             return  FemaleMeasurementInfo(**update)

@router.get('/favorites/{user_id}', response_model=FavoriteResponse)
async def get_user_favorite(
    user_id: str,
    current_user=Depends(get_current_user),
    db = Depends(get_db),
    user=Depends(get_user_by_id)
):
    if user_id != current_user.id:
        raise HTTPException(status_code=401, detail="Unauthorized request")
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found with the id")
    
    tailors = []
    products = []
    
    if user.favorites.get('tailors'):
        tailors = get_tailors(user.favorites['tailors'], db)
    
    if user.favorites.get('products'):
        products = get_products(user.favorites['products'], db)

    
    return FavoriteResponse(
        tailors=tailors,
        products=products
    )


@router.put('/favorites/{user_id}', response_model=SuccessMsg)
def update_user_favorite(req_body: AddFavorite, user_id: str, current_user=Depends(get_current_user),
                      db=Depends(get_db), user=Depends(get_user_by_id)):
    if user_id != current_user.id:
        raise HTTPException(status_code=401, detail="Unauthorized request")

    if  req_body.tailor_id:
        if not get_tailor_by_id(req_body.tailor_id, db):
            raise HTTPException(status_code=404, detail="tailor_id not valid")
    if req_body.product_id:
        if not _get_product(req_body.product_id, db):
            raise HTTPException(status_code=404, detail="product_id not valid")

    if not user:
        raise HTTPException(status_code=404, detail="User not found with the id")
    update = add_favorite(user_id, req_body, db)
    if not update:
        raise HTTPException(status_code=500, detail="An Error has occured")

    return update
