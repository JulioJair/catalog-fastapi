from sqlalchemy.orm import Session
from app import models
from fastapi import HTTPException
from .send_email import send_email_background


def response(detail=None):
    return {'detail': detail}

# In case we need to log emails sent
def write_notification(email: str, message=""):
    with open("log.txt", mode="w") as email_file:
        content = f"notification for {email}: {message}"
        email_file.write(content)


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


def update(db: Session, id, request, background_tasks):
    """
    Update product, will replace only the atributes in the request.
    """
    product = db.query(models.Product).get(id)
    if not product:
        raise HTTPException(status_code=404,
                            detail=f"Product with id {id} not found")
    import copy
    product_old_data = copy.deepcopy(product)
    # Partial update similar to PATCH verb
    if request.sku:
        product.sku = request.sku
    if request.name:
        product.name = request.name
    if request.price:
        product.price = request.price
    if request.brand:
        product.brand = request.brand

    # Retrieve all email addresses from admin users
    admin_emails = db.query(models.User.email).filter_by(is_admin=True).all()
    if admin_emails:
        # Convert 1-element tuple to a list
        emails_to = [i[0] for i in admin_emails]

        # Notify admins about product price changed
        send_email_background(
            background_tasks=background_tasks,
            subject='A product has been changed',
            emails_to=emails_to,
            body=f"""The product with id {id}
                sku: {product_old_data.sku} -> {product.sku}
                name: {product_old_data.name} -> {product.name}
                price: {product_old_data.price} -> {product.price}
                brand: {product_old_data.brand} -> {product.brand}
                """
        )
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
