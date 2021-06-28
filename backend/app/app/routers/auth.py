from fastapi import APIRouter, Depends, HTTPException, Query, Path

from typing import Optional, Any
from app import schemas, models, database
from sqlalchemy.orm import Session
from ..controllers import auth


router = APIRouter(
    prefix="/users",
    tags=["Users"],
    # dependencies=[Depends(get_token_header)],
    responses={404: {"description": "Product not found"}},
)
router = APIRouter(
    # prefix="/users",
    tags=["Authentication"],
    # dependencies=[Depends(get_token_header)],
    responses={404: {"description": "Product not found"}},
)


@router.post('/login')
def login(
    request: schemas.Login,
    db: Session = Depends(database.get_db)
):
    return auth.login(db, request)
