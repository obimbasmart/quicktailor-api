from fastapi import APIRouter, Depends, File, UploadFile, Form
from src.tailors.dependencies import get_current_tailor, get_current_user
from src.admin.dependencies import get_current_admin_or_tailor
from src.users.CRUD import get_users
from src.users.schemas import UserInfo
from dependencies import get_db
from typing import List, Tuple
from src.storage.aws_s3_storage import s3_client
from src.utils.schemas import ImageMetadata

router = APIRouter(
    prefix="/utils",
    tags=["utils"],
)


@router.post('/products/images/upload', response_model=None)
async def upload_product_images(images: List[UploadFile],
                                dimensions: str = Form(...),
                                tailor=Depends(get_current_tailor)):

    dimensions = eval(dimensions)
    image_keys = s3_client.upload_files(images, tailor.id, 'tailors/products')
    result = [
                {"url": url, "width": width, "height": height, "aspect_ratio": round(width/height, 2)}
                for url, (width, height) in zip(image_keys, dimensions)]

    return result


@router.post('/messages/media/upload', response_model=None)
async def upload_message_media(file: UploadFile,
                               user=Depends(get_current_user)):

    media_key = s3_client.upload_file(file, user.id, 'messages')
    url = s3_client.generate_presigned_url('get_object', media_key)
    return {'key': media_key, 'url': url}
