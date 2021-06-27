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


def success_response(data=None, datatype=None):
    return {'success': True, 'datatype': datatype, 'data': data}

def response(detail=None):
    return {'detail': detail}


@app.get("/products")
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
    return success_response(products, f'List of products, limited to {limit}')


@app.get("/products/{id}")
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
    return success_response(product, f'Product retrieved')


@app.post("/products")
def store_product(
        *,
        request: schemas.Product,
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
    return success_response(product, f'Product stored.')


@app.put("/products/{id}")
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
    return success_response(None, f"Product updated")


@app.delete("/products/{id}")
def delete_product(
    id: int = Query(..., description="The ID of the product to delete"),
    db: Session = Depends(get_db),
):
    """
    Destroy product record.
    """
    product = db.query(models.Product).get(id)
    if not product.first():
        raise HTTPException(
            status_code=404, detail=f"Product with id {id} not found")

    product.delete(synchronize_session=False)
    db.commit()
    return success_response()

# # # # # # # # # # # # # # #


@app.post("/users")
def store_user(
        *,
        request: schemas.User,
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
    return success_response(user, f'User stored.')


if __name__ == "__main__":
    uvicorn.run("main:app", host='0.0.0.0', reload=True)
