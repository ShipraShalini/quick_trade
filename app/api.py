from exception_handlers import EXCEPTION_HANDLERS_DICT
from fastapi import FastAPI

from app.controllers.order import OrderController
from app.models.order import CreateOrderModel, CreateOrderResponseModel
from app.response_types import APIResponse
from app.settings import settings
from app.tortoise_config import lifespan

app = FastAPI(
    title=settings.PROJECT_NAME,
    docs_url=f"/{settings.PROJECT_NAME}/docs",
    openapi_url=f"/{settings.PROJECT_NAME}/openapi.json",
    exception_handlers=EXCEPTION_HANDLERS_DICT,
    default_response_class=APIResponse,
    lifespan=lifespan,
)


@app.get("/healthcheck", status_code=200)
async def healthcheck() -> APIResponse:
    """
    Perform a health check for the application.

    This function returns an APIResponse indicating the health status
    of the application. It is used to verify that the application is
    running and able to respond to requests.

    Returns:
        APIResponse: A response object containing the status of the application.
    """
    return APIResponse({"status": "healthy"})


@app.post("/orders", status_code=201)
async def create_order(model: CreateOrderModel) -> CreateOrderResponseModel:
    # add versioning
    return await OrderController.create(model)
