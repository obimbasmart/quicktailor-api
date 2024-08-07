from fastapi import APIRouter, Depends, File, UploadFile
from src.tailors.dependencies import get_current_tailor, get_current_user
from src.admin.dependencies import get_current_admin_or_tailor
from src.users.CRUD import get_users
from src.users.schemas import UserInfo
from dependencies import get_db
from src.utils.CRUD import _get_list_of_fabrics
from src.utils.schemas import FabricItem
from typing import List
from src.storage.aws_s3_storage import s3_client

router = APIRouter(
    prefix="/utils",
    tags=["utils"],
)


@router.post('/products/images/upload', response_model=None)
async def upload_product_images(images: List[UploadFile],
                                tailor=Depends(get_current_tailor)):

    image_keys = s3_client.upload_files(images, tailor.id, 'tailors/products')
    urls = s3_client.generate_presigned_urls('get_object', image_keys.values())
    return \
        {
            f'img_{idx}': {
                'key': list(image_keys.values())[idx],
                "url": urls[idx]
            } for idx in range(len(image_keys))
        }


@router.post('/messages/media/upload', response_model=None)
async def upload_message_media(file: UploadFile,
                               user=Depends(get_current_user)):

    media_key = s3_client.upload_file(file, user.id, 'messages')
    url = s3_client.generate_presigned_url('get_object', media_key)
    return {'key': media_key, 'url': url}


@router.get('/products/fabrics', response_model=List[FabricItem])
async def get_list_of_fabrics(user=Depends(get_current_admin_or_tailor),
                              db=Depends(get_db)):
    fabrics = _get_list_of_fabrics(db)
    return fabrics
