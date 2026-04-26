from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session, joinedload
from typing import List, Optional
import os, shutil, uuid
from monolith.database import get_db
from monolith.models.message import Message
from monolith.models.user import User
from monolith.schemas.message import MessageCreate, MessageResponse, MessageStatusUpdate

router = APIRouter(prefix="/messages", tags=["messages"])

UPLOAD_DIR = "monolith/static/uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

def enrich(msg, db):
    user = db.query(User).filter(User.id == msg.sender_id).first()
    msg.sender_name = user.username if user else "Usuario"
    return msg

@router.post("/", response_model=MessageResponse, status_code=201)
def send_message(message_data: MessageCreate, sender_id: int, db: Session = Depends(get_db)):
    if not message_data.group_id and not message_data.receiver_id and not message_data.channel_id:
        raise HTTPException(status_code=400, detail="Debe especificar grupo, canal o receptor")
    message = Message(sender_id=sender_id, **message_data.model_dump())
    db.add(message)
    db.commit()
    db.refresh(message)
    return enrich(message, db)

@router.post("/upload", status_code=201)
async def upload_file(
    file: UploadFile = File(...),
    sender_id: int = Form(...),
    group_id: Optional[int] = Form(None),
    receiver_id: Optional[int] = Form(None),
    channel_id: Optional[int] = Form(None),
    db: Session = Depends(get_db)
):
    ext = os.path.splitext(file.filename)[1].lower()
    filename = f"{uuid.uuid4()}{ext}"
    filepath = os.path.join(UPLOAD_DIR, filename)
    with open(filepath, "wb") as f:
        shutil.copyfileobj(file.file, f)
    file_url = f"/static/uploads/{filename}"
    is_image = ext in [".jpg", ".jpeg", ".png", ".gif", ".webp"]
    msg_type = "image" if is_image else "file"
    message = Message(
        sender_id=sender_id,
        group_id=group_id,
        receiver_id=receiver_id,
        channel_id=channel_id,
        content=file.filename,
        file_url=file_url,
        message_type=msg_type,
        status="sent"
    )
    db.add(message)
    db.commit()
    db.refresh(message)
    return enrich(message, db)

@router.get("/group/{group_id}", response_model=List[MessageResponse])
def get_group_messages(group_id: int, db: Session = Depends(get_db)):
    msgs = db.query(Message).filter(Message.group_id == group_id).all()
    return [enrich(m, db) for m in msgs]

@router.get("/channel/{channel_id}", response_model=List[MessageResponse])
def get_channel_messages(channel_id: int, db: Session = Depends(get_db)):
    msgs = db.query(Message).filter(Message.channel_id == channel_id).all()
    return [enrich(m, db) for m in msgs]

@router.get("/direct/{user_id}/{other_user_id}", response_model=List[MessageResponse])
def get_direct_messages(user_id: int, other_user_id: int, db: Session = Depends(get_db)):
    msgs = db.query(Message).filter(
        ((Message.sender_id == user_id) & (Message.receiver_id == other_user_id)) |
        ((Message.sender_id == other_user_id) & (Message.receiver_id == user_id))
    ).all()
    return [enrich(m, db) for m in msgs]

@router.patch("/{message_id}/status", response_model=MessageResponse)
def update_status(message_id: int, status_data: MessageStatusUpdate, db: Session = Depends(get_db)):
    message = db.query(Message).filter(Message.id == message_id).first()
    if not message:
        raise HTTPException(status_code=404, detail="Mensaje no encontrado")
    message.status = status_data.status
    db.commit()
    db.refresh(message)
    return enrich(message, db)
