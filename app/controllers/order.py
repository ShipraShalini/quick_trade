from datetime import datetime
from uuid import UUID

from app.controllers.stock_exchange import OrderPlacementError, place_order
from app.models.order import CreateOrderModel, Order


class OrderController:
    @staticmethod
    async def create(model: CreateOrderModel) -> Order:
        """
        Creates a new order in the database and attempts to place it on the stock exchange.

        This method takes a `CreateOrderModel` instance, creates a new order in the database with
        the provided data, and attempts to place the order using the `place_order` function.
        If an `OrderPlacementError` is raised during the placement, the error is caught, and the
        order remains unplaced.

        Args:
            model (CreateOrderModel): The data required to create a new order.

        Returns:
            Order: The created order instance.
        """
        order = await Order.create(**model.model_dump(exclude_unset=True))
        await OrderController._place_order(order)
        return order

    @staticmethod
    async def place_failed_orders():
        """
        Attempts to place orders on the stock exchange that previously failed to be placed.

        This method retrieves all orders from the database where `order_placed_at` is null,
        indicating they have not been placed at the stock exchange. It then attempts to
        place each order using the `place_order` function. If an `OrderPlacementError` is
        raised, it is caught and the order remains unplaced. Otherwise, the order's
        `order_placed_at` field is updated to the current UTC time, and the order is saved.

        This operation could be enhanced by utilizing a task queue with retry logic
        to ensure reliability and scalability.
        """
        orders = await Order.filter(order_placed_at__isnull=True).all()
        for order in orders:
            await OrderController._place_order(order)

    @staticmethod
    async def _place_order(order: Order) -> None:
        """
        Places an order on the stock exchange.

        This method takes an `Order` instance and attempts to place it on the stock
        exchange using the `place_order` function. If the placement is successful, the
        order's `order_placed_at` field is updated to the current UTC time, and the
        order is saved in the database.

        Args:
            order (Order): The order to be placed on the stock exchange.
        """
        try:
            place_order(order)
        except OrderPlacementError:
            return
        order.order_placed_at = datetime.utcnow()
        await order.save()

    @staticmethod
    async def get_order_by_id(order_id: UUID) -> Order:
        """
        Retrieves an order by its unique identifier.

        This asynchronous method queries the database for an order with the specified
        `order_id`. If an order with the given ID exists, it returns the first match.
        Otherwise, it returns None.

        Args:
            order_id (UUID): The unique identifier of the order to retrieve.

        Returns:
            Order: The order instance with the specified ID, or None if no such order exists.
        """
        return await Order.filter(id=order_id).first()
