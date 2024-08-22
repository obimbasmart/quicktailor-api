from fastapi.responses import JSONResponse
from fastapi import status


def create_success_response(entity: str, data: dict = None):
    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content={"message": f"{entity} created successfully", "data": data}
    )


def update_success_response(entity: str, data: dict = None):
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={"message": f"{entity} updated successfully", "data": data}
    )


def delete_success_response(entity: str):
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={"message": f"{entity} deleted successfully"}
    )
