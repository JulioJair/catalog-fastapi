from fastapi import APIRouter, Depends, HTTPException, Query, Path

from typing import Optional, Any
from app import schemas, models, database, oauth2
from sqlalchemy.orm import Session
from app.hashing import Hash


router = APIRouter(
    responses={404: {"description": "Not found"}},
)


def response(detail=None):
    return {'detail': detail}


@router.get("/", tags=["Others"])
def root():
    return {"detail": "Catalog API"}


@router.post("/reset",tags=["Others"])
def reset(
    db: Session = Depends(database.get_db),
):
    """
    Reset tables and create default user.
    """
    # Drop table users
    user = db.query(models.User).delete()
    product = db.query(models.Product).delete()
    analytic = db.query(models.Analytic).delete()

    # Insert default user
    user = models.User(
        full_name='Julio',
        email='juliojair@outlook.com',
        hashed_password=Hash.bcrypt('12345678')
    )
    db.add(user)
    user = models.User(
        full_name='Admin',
        email='user@example.com',
        hashed_password=Hash.bcrypt('string')
    )
    db.add(user)
    product1 = models.Product(
        sku='PR1531',
        name='camera',
        price=400,
        brand='sony'
    )
    product2 = models.Product(
        sku='PR3548',
        name='camera',
        price=200,
        brand='nikon'
    )
    db.add(product1)
    db.add(product2)
    db.commit()
    analytic1 = models.Analytic(
        product_id=product1.id,
        times_requested=0,
    )
    analytic2 = models.Analytic(
        product_id=product2.id,
        times_requested=0,
    )
    db.add(analytic1)
    db.add(analytic2)
    db.commit()
    db.refresh(user)
    return user
