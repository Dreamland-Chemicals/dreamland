from pydantic import BaseModel, Field
from enum import Enum
from datetime import datetime
from src.utils import create_id


def create_date() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


class OrderStatus(Enum):
    PENDING = 'Pending'
    PROCESSING = 'Processing'
    SHIPPED = 'Shipped'
    DELIVERED = 'Delivered'
    CANCELLED = 'Cancelled'


class OrderItem(BaseModel):
    item_id: str = Field(default_factory=create_id)
    order_id: str
    product_id: str
    product_name: str
    price: int
    quantity: int
    discount_percent: int

    @property
    def total_price(self) -> int:
        """Calculate total price of the ordered products"""
        discounted_price = self.price - self.total_discount
        return int(discounted_price * self.quantity)

    @property
    def total_discount(self) -> int:
        return int(self.price * self.discount_percent / 100)


class Order(BaseModel):
    order_id: str = Field(default_factory=create_id)
    customer_id: str
    customer_name: str
    email: str
    phone: str
    address_id: str
    order_datetime: str = Field(default_factory=create_date)
    status: str = Field(default="Pending")

    items_ordered: list[OrderItem]

    @property
    def total_price(self) -> int:
        """Calculate total price of the order"""
        return sum(item.total_price for item in self.items_ordered)

    @property
    def quantity(self) -> int:
        """calculates total items on order"""
        return len(self.items_ordered)

    @property
    def time_since_ordered(self) -> int:
        """
            Calculates the time since order was placed in minutes
        """
        order_date = datetime.fromisoformat(self.order_datetime)
        time_difference = datetime.now() - order_date
        return int(time_difference.total_seconds() // 60)  # Convert to minutes