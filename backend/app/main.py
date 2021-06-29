from dotenv import load_dotenv
import uvicorn
from fastapi import FastAPI
from app import models
from app.database import engine
from app.routers import products, users, auth, analytics, misc

app = FastAPI()

models.Base.metadata.create_all(engine)


# Endpoints
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(products.router)
app.include_router(analytics.router)
app.include_router(misc.router)


if __name__ == "__main__":
    uvicorn.run("main:app", host='0.0.0.0', reload=True)
