from fastapi import FastAPI, status
from fastapi.responses import JSONResponse
from message_app.database import Base, engine
from fastapi.exceptions import RequestValidationError
from utils import format_validation_errors
from fastapi.testclient import TestClient
from message_app.src.messages.routers import router as message_router


def create_message_app():

    app = FastAPI()

    app.include_router(message_router)

    Base.metadata.create_all(bind=engine)

    @app.get("/")
    async def root():
        return {"message": "Hello, this is message app"}

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request, exc):
        return JSONResponse(format_validation_errors(exc), status.HTTP_422_UNPROCESSABLE_ENTITY)

    return app



app = create_message_app()
client = TestClient(app)