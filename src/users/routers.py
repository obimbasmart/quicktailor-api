from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.responses import JSONResponse
from src.auth.dependencies import get_current_user
from src.users.CRUD import get_users, update_user, update_measurement
from src.users.dependencies import get_user_by_id
from src.users.schemas import UserInfo, UpdateFields, SuccessMsg, FemaleMeasurementInfo,  MaleMeasurementInfo, MeasurementUpdate, KidMeasurementInfo
from dependencies import get_db
from typing import List, Union
from pydantic import UUID4, ValidationError
from src.users.utils import get_user_via_email
from src.users.constants import MEASUREMENT_TYPES
router = APIRouter(
    prefix="/users",
    tags=["users"],
)

@router.get('', response_model=List[UserInfo])
def get_all_users(current_user=Depends(get_current_user),
                    db=Depends(get_db)):
    users = get_users(db)
    return users

@router.get('/{user_id}', response_model=UserInfo)
def get_single_user(user_id: UUID4, current_user=Depends(get_current_user),
                      db=Depends(get_db), user=Depends(get_user_by_id)):
    if not user:
        raise HTTPException(status_code=404, detail="User not found with the id")
    return user
@router.put('/{user_id}', response_model=SuccessMsg)
def update_user_route(req_body: UpdateFields,  user_id: str, current_user=Depends(get_current_user),
                      db=Depends(get_db), user = Depends(get_user_by_id)):
    verify_email = get_user_via_email(req_body.email, db)
    if current_user.email == req_body.email:
        raise HTTPException(status_code=422, detail="This is your present Email")
    if verify_email:
        raise HTTPException(status_code=409, detail="Email is Already in use")
    print("request body",verify_email)
    if not user:
        raise HTTPException(status_code=404, detail="User not found with the id")
    if current_user.id != user_id:
        raise HTTPException(status_code=401, detail="Unauthorized request")

    update = update_user(user_id, req_body, db)
    return update

@router.get('/measurement/{user_id}', response_model=List[Union[MaleMeasurementInfo, FemaleMeasurementInfo, KidMeasurementInfo]])
def get_user_measurement(user_id: UUID4, current_user=Depends(get_current_user),
                      db=Depends(get_db), user=Depends(get_user_by_id)):
    if not user:
        raise HTTPException(status_code=404, detail="User not found with the id")
    formatted_measurements = []
    for measurement in user.measurement:
        if "measurement_type" in measurement and measurement['measurement_type'] == "male":    
            formatted_measurements.append(MaleMeasurementInfo(**measurement))
        if "measurement_type" in measurement and measurement['measurement_type'] == "female":
            formatted_measurements.append(FemaleMeasurementInfo(**measurement))
        if "measurement_type" in measurement and measurement['measurement_type'] == "kids":
            formatted_measurements.append(KidMeasurementInfo(**measurement))

    return formatted_measurements

@router.put('/measurement/{user_id}', response_model=Union[MaleMeasurementInfo, FemaleMeasurementInfo, KidMeasurementInfo])
def update_user_measurement(req_body: MeasurementUpdate, user_id: str, current_user=Depends(get_current_user),
                      db=Depends(get_db), user=Depends(get_user_by_id)):
    if user_id != current_user.id:
        print("this is user_id ", user_id, "this is current_user.id:  ", current_user.id)
        raise HTTPException(status_code=401, detail="Unauthorized request")
    if not user:
        raise HTTPException(status_code=404, detail="User not found with the id")
    update = update_measurement(user_id, req_body, db)
    if req_body.measurement_type not in MEASUREMENT_TYPES:
        raise HTTPException(status_code=422, detail="measurement_type not a valid type")
    update = update_measurement(user_id, req_body, db)
    if update:
        if update['measurement_type'] == "male":   
             return MaleMeasurementInfo(**update)
        elif update['measurement_type'] == "female":
             return  FemaleMeasurementInfo(**update)
        else:
             return KidMeasurementInfo(**update)

