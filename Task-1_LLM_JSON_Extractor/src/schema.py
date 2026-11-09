from typing import List
from pydantic import BaseModel


class LineItem(BaseModel):
    description: str
    quantity: int
    unit_price: float


class Invoice(BaseModel):
    vendor: str
    invoice_number: str
    date: str
    items: List[LineItem]
    total: float