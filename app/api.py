from typing import Optional

from fastapi import FastAPI
from pydantic import BaseModel, Field, condecimal, conint, constr, model_validator
from tortoise.contrib.fastapi import register_tortoise

from app.settings import settings, DB_CONFIG
from app.response_types import APIResponse
from app.models.order import OrderSide, OrderType, Order

app = FastAPI(
    title=settings.PROJECT_NAME,
    docs_url=f"/{settings.PROJECT_NAME}/docs",
    openapi_url=f"/{settings.PROJECT_NAME}/openapi.json",
    # exception_handlers=EXCEPTION_HANDLERS_DICT,
    default_response_class=APIResponse,
)

register_tortoise(
    app,
    config=DB_CONFIG,
    generate_schemas=False,
)


class CreateOrderModel(BaseModel):
    type_: OrderType = Field(..., alias="type")
    side: OrderSide
    instrument: constr(min_length=12, max_length=12)
    limit_price: Optional[condecimal(decimal_places=2)]
    quantity: conint(gt=0)

    @model_validator(mode='before')
    @classmethod
    def validator(cls, values: dict):
        if values.get("type_") == "market" and values.get("limit_price"):
            raise ValueError(
                "Providing a `limit_price` is prohibited for type `market`"
            )

        if values.get("type_") == "limit" and not values.get("limit_price"):
            raise ValueError("Attribute `limit_price` is required for type `limit`")

        return values


@app.get("/")
async def healthcheck() -> APIResponse:
    return APIResponse({"status": "healthy"})


class CreateOrderResponseModel(Order):
    pass


@app.post(
    "/orders",
    status_code=201,
    response_model=CreateOrderResponseModel,
    response_model_by_alias=True,
)
async def create_order(model: CreateOrderModel):
    # TODO: Add your implementation here
    raise NotImplementedError()
