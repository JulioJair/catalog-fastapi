from pydantic import BaseModel, Field


class AnalyticBase(BaseModel):
    times_requested: str = Field(
        description="Number of times the product has been queried by users")
    product_id: str = Field(description="Product id")


class ProductOut(BaseModel):
    from .user import UserOut
    sku: str = Field(description="Product identifier")
    name: str
    price: float
    brand: str
    editor: UserOut = None
    class Config():
        orm_mode = True

class Analytic(AnalyticBase):
    product: ProductOut = None
    class Config():
        orm_mode = True
