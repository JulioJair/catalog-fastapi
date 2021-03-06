from fastapi import APIRouter, Depends, HTTPException, Query, Path

from typing import Optional, Any
from app import schemas, models, database, oauth2
from sqlalchemy.orm import Session
from ..controllers import crud_user


router = APIRouter(
    prefix="/users",
    tags=["Users"],
    # dependencies=[Depends(get_token_header)],
    responses={404: {"description": "User not found"}},
)


def response(detail=None):
    return {'detail': detail}


@router.post("/", tags=[], response_model=schemas.UserOut)
def store_user(
        *,
        request: schemas.UserCreate,
        db: Session = Depends(database.get_db),
        get_current_user: schemas.UserOut = Depends(oauth2.get_current_user)
):
    """
    Create new user.
    """
    return crud_user.store(db, request=request)


@router.get("/{id}", tags=[], response_model=schemas.UserOut)
def show_user(
    id: int = Path(None, description="The ID of the user", gt=0),
    db: Session = Depends(database.get_db),
):
    """
    Show user.
    """
    return crud_user.show(db, id=id)


@router.put("/{id}", tags=[], response_model=schemas.UserOut)
def update_user(
        id: int,
        request: schemas.UserUpdate,
        db: Session = Depends(database.get_db),
        current_user: schemas.UserOut = Depends(oauth2.get_current_user)
):
    """
    Update user, will replace only the atributes in the request.
    """
    return crud_user.update(db, id=id, request=request)


@router.delete("/{id}", tags=[])
def delete_user(
    id: int = Query(..., description="The ID of the user to delete"),
    db: Session = Depends(database.get_db),
    current_user: schemas.UserOut = Depends(oauth2.get_current_user)
):
    """
    Destroy product record.
    """
    return crud_user.delete(db, id=id)
