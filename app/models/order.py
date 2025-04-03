from datetime import datetime
from decimal import Decimal
from enum import Enum
from typing import Optional
from uuid import UUID, uuid4

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    condecimal,
    conint,
    constr,
    model_validator,
)
from tortoise import Model, fields
from tortoise.contrib.pydantic import pydantic_model_creator


class OrderSide(Enum):
    BUY = "buy"
    SELL = "sell"


class OrderType(Enum):
    MARKET = "market"
    LIMIT = "limit"


class Order(Model):
    id: UUID = fields.UUIDField(pk=True, source_field="id", default=uuid4)
    type = fields.CharEnumField(OrderType)

    side = fields.CharEnumField(OrderSide)
    instrument: str = fields.CharField(max_length=12, minmax_length=12)
    limit_price: Optional[Decimal] = fields.DecimalField(max_digits=10, decimal_places=2, null=True)
    quantity: int = fields.IntField(min_value=1)
    created_at: datetime = fields.DatetimeField(auto_now_add=True)
    updated_at: datetime = fields.DatetimeField(auto_now=True)
    order_placed_at: Optional[datetime] = fields.DatetimeField(null=True)


class CreateOrderModel(BaseModel):
    type: OrderType = Field(alias="type")
    side: OrderSide
    instrument: constr(min_length=12, max_length=12)
    limit_price: Optional[condecimal(decimal_places=2)] = None
    quantity: conint(gt=0)

    class Config:
        use_enum_values = True

    @model_validator(mode="before")
    @classmethod
    def validator(cls, values: dict) -> None:
        """
        Validates the input values for creating an order.

        This function checks the values dictionary for consistency based on the order type.
        For 'market' type orders, it ensures that a `limit_price` is not provided.
        For 'limit' type orders, it ensures that a `limit_price` is provided.

        Args:
            cls: The class invoking the validator.
            values (dict): A dictionary containing the values to be validated.

        Returns:
            dict: The validated values dictionary.

        Raises:
            ValueError: If a `limit_price` is provided for a 'market' type order,
                        or if a `limit_price` is missing for a 'limit' type order.
        """
        if values.get("type") == "market" and values.get("limit_price"):
            raise ValueError("Providing a `limit_price` is prohibited for type `market`")

        if values.get("type") == "limit" and not values.get("limit_price"):
            raise ValueError("Attribute `limit_price` is required for type `limit`")

        return values


CreateOrderResponseModel = pydantic_model_creator(
    Order,
    exclude=("order_placed_at", "created_at", "updated_at"),
    model_config=ConfigDict(use_enum_values=True),
)
