from sqlalchemy.orm import Session
from app import schemas, models, database
from fastapi import HTTPException, status, Query
from app.hashing import Hash


def response(detail=None):
    return {'detail': detail}


def store(db, request=schemas.UserCreate):
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


def show(db: Session, id):
    """
    Show user data.
    """
    user = db.query(models.User).get(id)
    if not user:
        raise HTTPException(
            status_code=404, detail=f"User with id {id} not found")
    return user


def update(db: Session, id, request):
    """
    Update user, will replace only the atributes in the request.
    """
    user = db.query(models.User).get(id)
    if not user:
        raise HTTPException(status_code=404,
                            detail=f"User with id {id} not found")

    # Partial update similar to PATCH verb
    if request.full_name:
        user.full_name = request.full_name

    db.commit()
    return user


def delete(db: Session, id):
    """
    Destroy user record.
    """
    user = db.query(models.User).filter_by(id=id)
    if not user.first():
        raise HTTPException(
            status_code=404, detail=f"User with id {id} not found")

    user.delete(synchronize_session=False)
    db.commit()
    return response(f'User {id} deleted')
