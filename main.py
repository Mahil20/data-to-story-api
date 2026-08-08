from fastapi import FastAPI
from sqlmodel import SQLModel
from database import engine
from models import User
from routers import auth


app = FastAPI()

app.include_router(auth.router)

SQLModel.metadata.create_all(engine)

@app.get("/")
def home():
    return {"message": "Data-to-Story API is running!"}