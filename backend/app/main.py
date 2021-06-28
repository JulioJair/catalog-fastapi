from sqlalchemy.sql import schema
import uvicorn
from fastapi import FastAPI, Path, Query, HTTPException, Depends
from typing import Optional, Any
from app import schemas, models, database
from app.database import engine
from sqlalchemy.orm import Session
from app.hashing import Hash

app = FastAPI()

models.Base.metadata.create_all(engine)


@app.get("/")
def read_root():
    return {"detail": "Catalog API"}


get_db = database.get_db


def response(detail=None):
    return {'detail': detail}


@app.get("/products", tags=['Products'])
def index_products(
        db: Session = Depends(get_db),
        skip: int = Query(0, description="Apply offset to the query"),
        limit: int = Query(
            10, description="Set a limit of products retrieved"),
):
    """
    Retrieve products.
    """
    products = db.query(models.Product).offset(skip).limit(limit).all()
    return products


@app.get("/products/{id}", tags=['Products'])
def show_product(
    id: int = Path(None, description="The ID of the product", gt=0),
        db: Session = Depends(get_db)
):
    """
    Show product data.
    """
    product = db.query(models.Product).get(id)
    if not product:
        raise HTTPException(
            status_code=404, detail=f"Product with id {id} not found")
    return product


@app.post("/products", tags=['Products'])
def store_product(
        *,
        request: schemas.ProductCreate,
        db: Session = Depends(get_db),
):
    """
    Create new product.
    """
    product = models.Product(
        sku=request.sku,
        name=request.name,
        price=request.price,
        brand=request.brand
    )
    db.add(product)
    db.commit()
    db.refresh(product)
    return product


@app.put("/products/{id}", tags=['Products'], response_model=schemas.ProductOut)
def update_product(
        id: int,
        request: schemas.ProductUpdate,
        db: Session = Depends(get_db)
):
    """
    Update product, will replace only the atributes in the request.
    """
    product = db.query(models.Product).get(id)
    if not product:
        raise HTTPException(status_code=404,
                            detail=f"Product with id {id} not found")

    # Partial update similar to PATCH verb
    if request.sku:
        product.sku = request.sku
    if request.name:
        product.name = request.name
    if request.price:
        product.price = request.price
    if request.brand:
        product.brand = request.brand

    db.commit()
    return product


@app.delete("/products/{id}", tags=['Products'])
def delete_product(
    id: int = Query(..., description="The ID of the product to delete"),
    db: Session = Depends(get_db),
):
    """
    Destroy product record.
    """
    product = db.query(models.Product).filter_by(id=id)
    if not product.first():
        raise HTTPException(
            status_code=404, detail=f"Product with id {id} not found")

    product.delete(synchronize_session=False)
    db.commit()
    return response(f'Product {id} deleted')

# # # # # # # # # # # # # # #


@app.post("/users", tags=['Users'], response_model=schemas.UserOut)
def store_user(
        *,
        request: schemas.UserCreate,
        db: Session = Depends(get_db),
):
    """
    Create new user.
    """
    # Check if user already exists
    if db.query(models.User).filter_by(email=request.email).first():
        return response(f"User with mail '{request.email}' already exists")
    # Attempt to store the new user
    user = models.User(
        full_name=request.full_name,
        email=request.email,
        hashed_password=Hash.bcrypt(request.password)
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@app.get("/users/{id}", tags=['Users'], response_model=schemas.UserOut)
def show_user(
    id: int = Path(None, description="The ID of the user", gt=0),
    db: Session = Depends(get_db),
):
    """
    Show user.
    """
    user = db.query(models.User).get(id)
    if not user:
        raise HTTPException(
            status_code=404, detail=f"User with id {id} not found")
    return user


if __name__ == "__main__":
    uvicorn.run("main:app", host='0.0.0.0', reload=True)
