from unittest import mock
from uuid import UUID

import pytest
from controllers.stock_exchange import OrderPlacementError
from exception_handlers import DEFAULT_PROD_CLIENT_ERROR_MESSAGE


@pytest.mark.asyncio
@mock.patch("controllers.order.place_order")
async def test_create_order(mock_place_order, client):
    # Arrange
    mock_place_order.return_value = None
    data = {
        "type": "market",
        "side": "sell",
        "instrument": "XRPUSDT00006",
        "quantity": 500,
    }

    # Act
    response = client.post("/orders", json=data)

    # Assert
    assert response.status_code == 201
    response_data = response.json()
    assert response_data["success"] is True
    order_id = response_data["data"].pop("id", None)
    assert UUID(order_id)
    assert response_data["data"] == {**data, "limit_price": None}

    # todo: fix test database
    # order = await OrderController.get_order_by_id(order_id)
    # assert order
    # assert order.order_placed_at is not None


@pytest.mark.parametrize(
    "data_in",
    [
        {"side": "BUY"},
        {"type": "LIMIT"},
        {"instrument": "INSTRUMENT"},
        {"quantity": "abc"},
        {"type": "limit"},
    ],
)
@pytest.mark.asyncio
@mock.patch("app.controllers.order.place_order")
async def test_create_order_limit_price_error(mock_place_order, client, data_in):
    # Arrange
    data = {
        "type": "market",
        "side": "buy",
        "instrument": "DOTUSDT00008",
        "quantity": 75,
    }
    data = {**data, **data_in}

    # Act
    response = client.post("/orders", json=data)

    # Assert
    assert response.status_code == 400
    response_data = response.json()
    assert response_data["success"] is False
    assert response_data["error"] == {"message": DEFAULT_PROD_CLIENT_ERROR_MESSAGE}

    # todo: fix test database
    # order = await OrderController.get_order_by_id(order_id)
    # assert order is None


@pytest.mark.asyncio
@mock.patch("controllers.order.place_order")
async def test_create_order_place_order_error(mock_place_order, client):
    # Arrange
    mock_place_order.side_effect = OrderPlacementError("Invalid order placement")
    data = {
        "type": "market",
        "side": "sell",
        "instrument": "XRPUSDT00006",
        "quantity": 500,
    }

    # Act
    response = client.post("/orders", json=data)

    # Assert
    assert response.status_code == 201
    response_data = response.json()
    assert response_data["success"]
    order_id = response_data["data"].pop("id", None)
    assert UUID(order_id)
    assert response_data["data"] == {**data, "limit_price": None}

    # todo: fix test database
    # order = await OrderController.get_order_by_id(order_id)
    # assert order
    # assert order.order_placed_at is None
