from sqlalchemy.orm import Session
from app import schemas, models, database
from fastapi import HTTPException, status, Query


def response(detail=None):
    return {'detail': detail}


def index(db: Session, skip: int = 0, limit: int = 10):
    """
    Retrieve products.
    """
    products = db.query(models.Product).offset(skip).limit(limit).all()
    return products


def show(db: Session, id):
    """
    Show product data.
    """
    product = db.query(models.Product).get(id)
    if not product:
        raise HTTPException(
            status_code=404, detail=f"Product with id {id} not found")

    # Count every query to each product_id
    # feat: A condition to avoid counting from same user in less than one hour would be great
    analytic = db.query(models.Analytic).filter_by(
        product_id=product.id).first()
    analytic.times_requested = analytic.times_requested + 1
    db.commit()
    return product


def store(db: Session, request):
    """
    Create new product.
    """
    # Store product
    product = models.Product(
        sku=request.sku,
        name=request.name,
        price=request.price,
        brand=request.brand
    )
    db.add(product)
    db.commit()

    # Store analytic data for current product
    analytic = models.Analytic(
        product_id=product.id,
        times_requested=0,
    )
    db.add(analytic)
    db.commit()

    db.refresh(product)
    return product


def update(db: Session, id, request):
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


def delete(db: Session, id):
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
