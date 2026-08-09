from fastapi import FastAPI
from sqlmodel import SQLModel
from database import engine
from models import User
from routers import auth
from routers import datasets
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(datasets.router)
app.include_router(auth.router)


SQLModel.metadata.create_all(engine)

@app.get("/")
def home():
    return {"message": "Data-to-Story API is running!"}