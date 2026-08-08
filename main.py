from fastapi import FastAPI
from sqlmodel import SQLModel
from database import engine

app = FastAPI()

SQLModel.metadata.create_all(engine)

@app.get("/")
def home():
    return {"message": "Data-to-Story API is running!"}