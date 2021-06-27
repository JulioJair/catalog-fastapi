from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Float
from .database import Base
from sqlalchemy.orm import relationship

# from app import database

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean(), default=False)

    # products = relationship("Product", back_populates="editor")


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    sku = Column(String, index=True)
    name = Column(String, index=True)
    price = Column(Float)
    brand = Column(String, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))

    # editor = relationship("User", back_populates="products")
