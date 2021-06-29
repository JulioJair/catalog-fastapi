from fastapi import APIRouter, Depends, HTTPException, status, Query, Path, BackgroundTasks

from typing import Optional, Any
from app import schemas, models, database, oauth2
from sqlalchemy.orm import Session
from ..controllers import crud_analytic

router = APIRouter(
    prefix="/analytics",
    tags=["Analytics"],
    # dependencies=[Depends(get_token_header)],
    responses={404: {"description": "Analytic data not found"}},
)


@router.get("/", tags=[])
def index(
        db: Session = Depends(database.get_db),
        skip: int = Query(0, description="Apply offset to the query"),
        limit: int = Query(
            10, description="Set a limit of data retrieved"),
):
    """
    Retrieve product analytics.
    """
    return crud_analytic.index(db, skip=skip, limit=limit)
