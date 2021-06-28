from sqlalchemy.orm import Session
from app import schemas, models, database, token
from fastapi import HTTPException, status, Query
from app.hashing import Hash


def login(db, request):
    user = db.query(models.User).filter_by(email=request.email).first()
    if not user:
        raise HTTPException(status_code=404, detail=f"User not found")
    if not Hash.verify(user.hashed_password, request.password):
        raise HTTPException(status_code=404, detail=f"Incorrect password")

    access_token = token.create_access_token(
        data={"sub": user.email},
    )
    return {"access_token": access_token, "token_type": "bearer"}

    return login
