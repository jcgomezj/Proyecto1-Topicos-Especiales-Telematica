from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from core.database import get_db
from models.user import UserProfile
from schemas.user import UserProfileCreate, UserProfileUpdate, UserProfileResponse, PresenceUpdate

router = APIRouter(prefix="/users", tags=["users"])

@router.post("/", response_model=UserProfileResponse, status_code=status.HTTP_201_CREATED)
def create_profile(profile_data: UserProfileCreate, db: Session = Depends(get_db)):
    if db.query(UserProfile).filter(UserProfile.user_id == profile_data.user_id).first():
        raise HTTPException(status_code=400, detail="Perfil ya existe")
    new_profile = UserProfile(**profile_data.model_dump())
    db.add(new_profile)
    db.commit()
    db.refresh(new_profile)
    return new_profile

@router.get("/{user_id}", response_model=UserProfileResponse)
def get_profile(user_id: int, db: Session = Depends(get_db)):
    profile = db.query(UserProfile).filter(UserProfile.user_id == user_id).first()
    if not profile:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return profile

@router.put("/{user_id}", response_model=UserProfileResponse)
def update_profile(user_id: int, profile_data: UserProfileUpdate, db: Session = Depends(get_db)):
    profile = db.query(UserProfile).filter(UserProfile.user_id == user_id).first()
    if not profile:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    for key, value in profile_data.model_dump(exclude_unset=True).items():
        setattr(profile, key, value)
    db.commit()
    db.refresh(profile)
    return profile

@router.get("/", response_model=List[UserProfileResponse])
def get_all_users(db: Session = Depends(get_db)):
    return db.query(UserProfile).all()

@router.patch("/presence", response_model=UserProfileResponse)
def update_presence(presence_data: PresenceUpdate, db: Session = Depends(get_db)):
    profile = db.query(UserProfile).filter(UserProfile.user_id == presence_data.user_id).first()
    if not profile:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    profile.is_online = presence_data.is_online
    db.commit()
    db.refresh(profile)
    return profile
