from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from jose import jwt
import os, datetime
from database import get_db
from models import User

router = APIRouter(prefix="/auth", tags=["auth"])
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
SECRET = os.getenv("JWT_SECRET", "your-secret-key")

@router.post("/register")
def register(email: str, password: str, name: str, db: Session = Depends(get_db)):
    if db.query(User).filter(User.email == email).first():
        raise HTTPException(400, "Email already registered")
    user = User(email=email, hashed_pw=pwd_context.hash(password), name=name)
    db.add(user)
    db.commit()
    return {"message": "Registered successfully"}

@router.post("/login")
def login(email: str, password: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == email).first()
    if not user or not pwd_context.verify(password, user.hashed_pw):
        raise HTTPException(401, "Invalid credentials")
    token = jwt.encode(
        {"sub": str(user.id), "exp": datetime.datetime.utcnow() + datetime.timedelta(days=7)},
        SECRET, algorithm="HS256"
    )
    return {"access_token": token, "name": user.name}