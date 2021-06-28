from fastapi import APIRouter, Depends, HTTPException, Query, Path

from typing import Optional, Any
from app import schemas, models, database
from sqlalchemy.orm import Session
from app.hashing import Hash


router = APIRouter(
    prefix="/users",
    tags=["Users"],
    # dependencies=[Depends(get_token_header)],
    responses={404: {"description": "Product not found"}},
)


def response(detail=None):
    return {'detail': detail}


@router.post("/", tags=[], response_model=schemas.UserOut)
def store_user(
        *,
        request: schemas.UserCreate,
        db: Session = Depends(database.get_db),
):
    """
    Create new user.
    """
    # Check if user already exists
    if db.query(models.User).filter_by(email=request.email).first():
        raise HTTPException(
            status_code=400, detail=f"User with mail '{request.email}' already exists")
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


@router.get("/{id}", tags=[], response_model=schemas.UserOut)
def show_user(
    id: int = Path(None, description="The ID of the user", gt=0),
    db: Session = Depends(database.get_db),
):
    """
    Show user.
    """
    user = db.query(models.User).get(id)
    if not user:
        raise HTTPException(
            status_code=404, detail=f"User with id {id} not found")
    return user
