import uvicorn
from fastapi import FastAPI
from app import models
from app.database import engine
from app.routers import products, users, auth

app = FastAPI()

models.Base.metadata.create_all(engine)


@app.get("/")
def root():
    return {"detail": "Catalog API"}


# Endpoints
app.include_router(auth.router)
app.include_router(products.router)
app.include_router(users.router)


if __name__ == "__main__":
    uvicorn.run("main:app", host='0.0.0.0', reload=True)
