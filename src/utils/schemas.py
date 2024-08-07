from pydantic import BaseModel

class ImageItem(BaseModel):
    key: str
    url: str

class ProductUploadImageResponse(BaseModel):
    str: ImageItem


class FabricItem(BaseModel):
    id: str
    name: str

class FabricItemUpload(BaseModel):
    name: str

class FabricItemUpdate(BaseModel):
    new_name: str