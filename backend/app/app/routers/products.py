from fastapi import APIRouter, Depends, HTTPException, status, Query, Path

from typing import Optional, Any
from app import schemas, models, database
from sqlalchemy.orm import Session
from ..controllers import crud_product

# from ..dependencies import get_token_header

router = APIRouter(
    prefix="/products",
    tags=["Products"],
    # dependencies=[Depends(get_token_header)],
    responses={404: {"description": "Product not found"}},
)


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
    return crud_product.index(db, skip=skip, limit=limit)


@router.get("/{id}", tags=[], response_model=schemas.ProductOut)
def show_product(
    id: int = Path(None, description="The ID of the product", gt=0),
        db: Session = Depends(database.get_db)
):
    """
    Show product data.
    """
    return crud_product.show(db, id=id)


@router.post("/", status_code=status.HTTP_201_CREATED, tags=[])
def store_product(
        *,
        request: schemas.ProductCreate,
        db: Session = Depends(database.get_db),
):
    """
    Create new product.
    """
    return crud_product.store(db, request=request)


@router.put("/{id}", tags=[], response_model=schemas.ProductOut)
def update_product(
        id: int,
        request: schemas.ProductUpdate,
        db: Session = Depends(database.get_db)
):
    """
    Update product, will replace only the atributes in the request.
    """
    return crud_product.update(db, id=id, request=request)


@router.delete("/{id}", tags=[])
def delete_product(
    id: int = Query(..., description="The ID of the product to delete"),
    db: Session = Depends(database.get_db),
):
    """
    Destroy product record.
    """
    return crud_product.delete(db, id=id)
