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
    Retrieve products analytics.
    """
    analytics = db.query(models.Analytic).offset(skip).limit(limit).all()
    return analytics


def show(db: Session, id):
    """
    Show product data.
    """
    product = db.query(models.Product).get(id)
    if not product:
        raise HTTPException(
            status_code=404, detail=f"Product with id {id} not found")
    analytic = db.query(models.Analytic).filter_by(
        product_id=product.id).first()
    # analytic.name = product.name
    # analytic.sku = product.sku
    return analytic

