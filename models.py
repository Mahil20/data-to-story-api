from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime

class User(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    username: str
    hashed_password: str

class Dataset(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    filename: str
    row_count: int
    columns: str
    uploaded_at: datetime = Field(default_factory=datetime.utcnow)
    owner_id: int = Field(foreign_key="user.id")