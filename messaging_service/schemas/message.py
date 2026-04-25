from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class MessageCreate(BaseModel):
    content: Optional[str] = None
    message_type: str = "text"
    group_id: Optional[int] = None
    channel_id: Optional[int] = None
    receiver_id: Optional[int] = None

class MessageResponse(BaseModel):
    id: int
    sender_id: int
    content: Optional[str]
    message_type: str
    status: str
    group_id: Optional[int]
    channel_id: Optional[int]
    receiver_id: Optional[int]
    created_at: datetime
    class Config:
        from_attributes = True

class MessageStatusUpdate(BaseModel):
    status: str

class FileResponse(BaseModel):
    id: int
    message_id: int
    filename: str
    file_url: str
    file_size: Optional[int]
    file_type: Optional[str]
    uploaded_at: datetime
    class Config:
        from_attributes = True
