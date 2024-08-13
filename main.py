from fastapi import FastAPI, status
from fastapi.responses import JSONResponse
from src.auth.routers import router as auth_router
from src.tailors.routers import router as tailor_router
from src.products.routers import router as product_router
from src.users.routers import router as user_router
from src.admin.routers import router as admin_router
from src.orders.routers import router as orders_router
from src.utils.routers import router as utils_router
from database import Base, engine
from fastapi.exceptions import RequestValidationError
from utils import format_validation_errors
from fastapi.testclient import TestClient



def create_app():

    app = FastAPI()

    app.include_router(auth_router)
    app.include_router(tailor_router)
    app.include_router(product_router)
    app.include_router(user_router)
    app.include_router(admin_router)
    app.include_router(utils_router)
    app.include_router(orders_router)

    Base.metadata.create_all(bind=engine)

    @app.get("/")
    async def root():
        return {"message": "Hello World"} 

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request, exc):
        return JSONResponse(format_validation_errors(exc), status.HTTP_422_UNPROCESSABLE_ENTITY)
    
    return app

   

app = create_app()
client = TestClient(app)
