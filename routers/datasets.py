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

@router.get("/datasets/{dataset_id}/stats")
def get_dataset_stats(dataset_id: int, current_user: str = Depends(get_current_user)):
    with Session(engine) as session:
        dataset = session.exec(select(Dataset).where(Dataset.id == dataset_id)).first()
        if not dataset:
            raise HTTPException(status_code=404, detail="Dataset not found")

        user = session.exec(select(User).where(User.username == current_user)).first()
        if dataset.owner_id != user.id:
            raise HTTPException(status_code=403, detail="You don't own this dataset")

    file_path = f"uploads/{dataset.filename}"
    df = pd.read_csv(file_path)

    numeric_columns = df.select_dtypes(include="number").columns

    stats = {}
    for col in numeric_columns:
      stats[col] = {
        "mean": round(float(df[col].mean()), 2),
        "min": round(float(df[col].min()), 2),
        "max": round(float(df[col].max()), 2),
        "sum": round(float(df[col].sum()), 2)
    }

    correlations_raw = df[numeric_columns].corr().round(2).to_dict()
    correlations = {
    col1: {col2: float(value) for col2, value in inner.items()}
    for col1, inner in correlations_raw.items()
    }

    return {
        "dataset_id": dataset.id,
        "filename": dataset.filename,
        "row_count": dataset.row_count,
        "stats": stats,
        "correlations": correlations
    }