import socketio
from fastapi import FastAPI, status
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from src.auth.routers import router as auth_router
from src.tailors.routers import router as tailor_router
from src.products.routers import router as product_router
from src.users.routers import router as user_router
from src.admin.routers import router as admin_router
from src.messages.routers import router as message_router
from src.notifications.routers import router as notification_router
from src.utils.routers import router as utils_router
from src.payments.routers import router as payment_router
from database import Base, engine
from fastapi.exceptions import RequestValidationError
from utils import format_validation_errors
from fastapi.testclient import TestClient
from socket_server import sio


def create_app():
    app = FastAPI()

    # Apply CORS Middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # Adjust according to your frontend domain
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


    # Include your routers
    app.include_router(auth_router)
    app.include_router(tailor_router)
    app.include_router(product_router)
    app.include_router(user_router)
    app.include_router(admin_router)
    app.include_router(utils_router)
    app.include_router(payment_router)
    app.include_router(message_router)
    app.include_router(notification_router)

    # Create database tables
    Base.metadata.create_all(bind=engine)

    @app.get("/")
    async def root():
        return {"message": "Hello World"}

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request, exc):
        return JSONResponse(format_validation_errors(exc), status.HTTP_422_UNPROCESSABLE_ENTITY)

    # Wrap the FastAPI app with the Socket.IO ASGIApp
    return socketio.ASGIApp(sio, app)

app = create_app()

client = TestClient(app)

