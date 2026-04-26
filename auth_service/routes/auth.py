from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import timedelta
from core.database import get_db
from core.security import verify_password, get_password_hash, create_access_token
from models.user import User
from schemas.user import UserCreate, UserLogin, UserResponse, Token
from core.config import settings
from kafka_producer import publish_presence_event

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register(user_data: UserCreate, db: Session = Depends(get_db)):
    if db.query(User).filter(User.email == user_data.email).first():
        raise HTTPException(status_code=400, detail="Email ya registrado")
    if db.query(User).filter(User.username == user_data.username).first():
        raise HTTPException(status_code=400, detail="Username ya en uso")
    new_user = User(username=user_data.username, email=user_data.email, hashed_password=get_password_hash(user_data.password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.post("/login", response_model=Token)
def login(user_data: UserLogin, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == user_data.email).first()
    if not user or not verify_password(user_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Credenciales invalidas")
    user.is_online = True
    db.commit()
    access_token = create_access_token(data={"sub": user.email}, expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES))
    publish_presence_event(user.email, "online")
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/logout")
def logout(email: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == email).first()
    if user:
        user.is_online = False
        db.commit()
    publish_presence_event(email, "offline")
    return {"message": "Sesion cerrada exitosamente"}
