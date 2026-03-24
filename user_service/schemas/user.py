from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

class UserProfileCreate(BaseModel):
    user_id: int
    username: str
    email: EmailStr
    bio: Optional[str] = None
    avatar_url: Optional[str] = None

class UserProfileUpdate(BaseModel):
    bio: Optional[str] = None
    avatar_url: Optional[str] = None

class UserProfileResponse(BaseModel):
    id: int
    user_id: int
    username: str
    email: str
    bio: Optional[str]
    avatar_url: Optional[str]
    is_online: bool
    last_seen: datetime
    created_at: datetime
    class Config:
        from_attributes = True

class PresenceUpdate(BaseModel):
    user_id: int
    is_online: bool
