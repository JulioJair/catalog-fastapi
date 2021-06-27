from pydantic import BaseModel, Field
from typing import Optional
from fastapi import Path

# Shared properties
class ProductBase(BaseModel):
    sku: str = Field(description="Product identifier")
    name: str
    price: float
    brand: Optional[str]


# Properties shared by models stored in DB
class Product(ProductBase):
    class Config():
        orm_mode = True


# Properties to receive via API on update
class ProductUpdate(ProductBase):
    sku: Optional[str]
    name: Optional[str]
    price: Optional[float]
    brand: Optional[str]


# Properties to return to client
class ProductIndex(Product):
    pass


# Properties to return to client
class ProductShow(Product):
    pass


