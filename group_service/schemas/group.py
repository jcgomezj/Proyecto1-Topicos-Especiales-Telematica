from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class GroupCreate(BaseModel):
    name: str
    description: Optional[str] = None
    group_type: str = "public"

class GroupResponse(BaseModel):
    id: int
    name: str
    description: Optional[str]
    group_type: str
    created_by: int
    created_at: datetime
    class Config:
        from_attributes = True

class GroupMemberCreate(BaseModel):
    user_id: int
    role: str = "member"

class GroupMemberResponse(BaseModel):
    id: int
    group_id: int
    user_id: int
    role: str
    joined_at: datetime
    class Config:
        from_attributes = True

class ChannelCreate(BaseModel):
    name: str
    description: Optional[str] = None

class ChannelResponse(BaseModel):
    id: int
    group_id: int
    name: str
    description: Optional[str]
    created_at: datetime
    class Config:
        from_attributes = True
