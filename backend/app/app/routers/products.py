from fastapi import APIRouter, Depends, HTTPException, status, Query, Path

from typing import Optional, Any
from app import schemas, models, database
from sqlalchemy.orm import Session

# from ..dependencies import get_token_header

router = APIRouter(
    prefix="/products",
    tags=["Products"],
    # dependencies=[Depends(get_token_header)],
    responses={404: {"description": "Product not found"}},
)

def response(detail=None):
    return {'detail': detail}


@router.get("/", tags=[])
def index_products(
        db: Session = Depends(database.get_db),
        skip: int = Query(0, description="Apply offset to the query"),
        limit: int = Query(
            10, description="Set a limit of products retrieved"),
):
    """
    Retrieve products.
    """
    products = db.query(models.Product).offset(skip).limit(limit).all()
    return products


@router.get("/{id}", tags=[], response_model=schemas.ProductOut)
def show_product(
    id: int = Path(None, description="The ID of the product", gt=0),
        db: Session = Depends(database.get_db)
):
    """
    Show product data.
    """
    product = db.query(models.Product).get(id)
    if not product:
        raise HTTPException(
            status_code=404, detail=f"Product with id {id} not found")
    return product


@router.post("/", status_code=status.HTTP_201_CREATED, tags=[])
def store_product(
        *,
        request: schemas.ProductCreate,
        db: Session = Depends(database.get_db),
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


@router.put("/{id}", tags=[], response_model=schemas.ProductOut)
def update_product(
        id: int,
        request: schemas.ProductUpdate,
        db: Session = Depends(database.get_db)
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


@router.delete("/{id}", tags=[])
def delete_product(
    id: int = Query(..., description="The ID of the product to delete"),
    db: Session = Depends(database.get_db),
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