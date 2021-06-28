from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Float, DateTime
from .database import Base
from sqlalchemy.orm import relationship
import datetime


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    is_admin = Column(Boolean, default=True)

    products = relationship("Product", back_populates="editor")


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    sku = Column(String, index=True)
    name = Column(String, index=True)
    price = Column(Float)
    brand = Column(String, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow)

    editor = relationship("User", back_populates="products")
    analytic = relationship("Analytic", back_populates="product")


class Analytic(Base):
    __tablename__ = "analytics"

    id = Column(Integer, primary_key=True, index=True)
    times_requested = Column(Integer, index=True)
    product_id = Column(Integer, ForeignKey("products.id"))

    product = relationship("Product", back_populates="editor")
