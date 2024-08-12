

from fastapi import APIRouter, Depends, status, Path
from src.admin.dependencies import get_current_admin
from typing import Set
from src.admin.CRUD import _create_fabrics, _delete_fabric, _update_fabric, _get_tailors, _get_users, _get_user, _get_tailor, _update_tailor
from src.admin.schemas import AdminTailorListItem, AdminUserListItem, AdminTailorItem, AdminTailorUpdate
from src.admin.utils import TailorState
from dependencies import get_db
from fastapi.responses import JSONResponse
from src.utils.schemas import FabricItemUpdate
from typing import List

router = APIRouter(
    prefix="/admin",
    tags=["admin"],
)


@router.get('/tailors', response_model=List[AdminTailorListItem])
async def get_tailors(current_user=Depends(get_current_admin),
                      db=Depends(get_db)):
    tailors = _get_tailors(db)
    return tailors


@router.get('/tailors/{tailor_id}', response_model=AdminTailorItem)
async def get_tailor(tailor_id: str,
                     current_user=Depends(get_current_admin),
                     db=Depends(get_db)):
    tailor = _get_tailor(tailor_id, db)
    return tailor


@router.get('/users', response_model=List[AdminUserListItem])
async def get_users(current_user=Depends(get_current_admin),
                    db=Depends(get_db)):
    users = _get_users(db)
    return users


@router.post('/products/fabrics', response_model=None)
async def create_fabrics(fabrics: Set[str],
                         current_user=Depends(get_current_admin),
                         db=Depends(get_db)):
    fabric_names = _create_fabrics(fabrics, db)
    return {"message": "success", "fabrics": fabric_names}


@router.delete('/products/fabrics/{name}', response_model=None)
async def delete_fabric(name: str,
                        current_user=Depends(get_current_admin),
                        db=Depends(get_db)):

    fabric_names = _delete_fabric(name, db)
    return JSONResponse(status_code=status.HTTP_200_OK, content={'message': 'Deleted successfully'})


@router.put('/products/fabrics/{name}', response_model=None)
async def update_fabric(name: str,
                        req_body: FabricItemUpdate,
                        current_user=Depends(get_current_admin),
                        db=Depends(get_db)):

    fabric_names = _update_fabric(name, req_body.new_name, db)
    return JSONResponse(status_code=status.HTTP_200_OK, content={'message': 'Updated successfully'})



@router.patch('/tailors/{tailor_id}/verify')
async def update_tailor(tailor_id: str,
                        current_user=Depends(get_current_admin),
                        db=Depends(get_db)):
    update = _update_tailor(tailor_id, TailorState.VERIFY, db)
    
    return JSONResponse(status_code=status.HTTP_200_OK,
                        content={"message": 'Update successfull'})


@router.patch('/tailors/{tailor_id}/suspend')
async def update_tailor(tailor_id: str,
                        current_user=Depends(get_current_admin),
                        db=Depends(get_db)):
    update = _update_tailor(tailor_id, TailorState.SUSPEND, db)
    
    return JSONResponse(status_code=status.HTTP_200_OK,
                        content={"message": 'Update successfull'})