from pydantic import BaseModel

class ImageItem(BaseModel):
    key: str
    url: str

class ProductUploadImageResponse(BaseModel):
    str: ImageItem


class ImageMetadata(BaseModel):
    width: int
    height: int
    type: str