from pydantic import BaseModel, Field
from typing import Optional
from fastapi import Path
import datetime


class AnalyticBase(BaseModel):
    product_id: str = Field(description="Product id")
    times_requested: str = Field(
        description="Number of times the product has been queried by users")


class Analytic(AnalyticBase):
    product_id: str = Field(description="Product id")
    times_requested: str = Field(
        description="Number of times the product has been queried by users")

    class Config():
        orm_mode = True
