from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from sqlmodel import Session
from database import engine
from models import Dataset, User
from auth import get_current_user
from sqlmodel import select
import pandas as pd
import os

router = APIRouter()

@router.post("/datasets/upload")
def upload_dataset(file: UploadFile = File(...), current_user: str = Depends(get_current_user)):
    if not file.filename.endswith(".csv"):
        raise HTTPException(status_code=400, detail="Only CSV files are allowed")

    file_path = f"uploads/{file.filename}"
    with open(file_path, "wb") as f:
        f.write(file.file.read())

    df = pd.read_csv(file_path)

    with Session(engine) as session:
        user = session.exec(select(User).where(User.username == current_user)).first()
        new_dataset = Dataset(
            filename=file.filename,
            row_count=len(df),
            columns=",".join(df.columns),
            owner_id=user.id
        )
        session.add(new_dataset)
        session.commit()
        session.refresh(new_dataset)

    return {
        "message": "Dataset uploaded successfully",
        "dataset_id": new_dataset.id,
        "rows": new_dataset.row_count,
        "columns": new_dataset.columns
    }