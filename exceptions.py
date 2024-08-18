from fastapi import HTTPException, status


def not_found_exception(entity: str = "Entity"):
    return HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"{entity} not found"
    )


def access_denied_exception():
    return HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Access denied"
    )


def unauthorized_access_exception():
    return HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Unauthorized access"
    )

def already_exists_exception(resource_name: str = "Resource"):
    return HTTPException(
        status_code=status.HTTP_409_CONFLICT,
        detail=f"{resource_name} already exists."
    )

