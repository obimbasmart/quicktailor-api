from fastapi import HTTPException, status


def not_found_exception(entity: str = "Entity"):
    return HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"{entity} not found"
    )


def access_denied_exception(msg: str = None):
    
    return HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail=msg if msg else "Access denied"
    )


def unauthorized_access_exception(msg: str = None):
    return HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail= msg if msg else "Unauthorized access"
    )

def already_exists_exception(resource_name: str = "Resource"):
    return HTTPException(
        status_code=status.HTTP_409_CONFLICT,
        detail=f"{resource_name} already exists."
    )

