from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session, select
from database import engine
from models import User
from auth import hash_password, verify_password, create_access_token

router = APIRouter()

@router.post("/signup")
def signup(username: str, password: str):
    with Session(engine) as session:
        existing_user = session.exec(select(User).where(User.username == username)).first()
        if existing_user:
            raise HTTPException(status_code=400, detail="Username already taken")

        new_user = User(username=username, hashed_password=hash_password(password))
        session.add(new_user)
        session.commit()
        session.refresh(new_user)
    return {"message": "User created successfully", "user_id": new_user.id}


@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    with Session(engine) as session:
        user = session.exec(select(User).where(User.username == form_data.username)).first()
        if not user or not verify_password(form_data.password, user.hashed_password):
            raise HTTPException(status_code=401, detail="Invalid username or password")

        token = create_access_token({"sub": user.username})
    return {"access_token": token, "token_type": "bearer"}