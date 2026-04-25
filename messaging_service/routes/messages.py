from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from core.database import get_db
from models.message import Message
from schemas.message import MessageCreate, MessageResponse, MessageStatusUpdate

router = APIRouter(prefix="/messages", tags=["messages"])

@router.post("/", response_model=MessageResponse, status_code=201)
def send_message(message_data: MessageCreate, sender_id: int, db: Session = Depends(get_db)):
    if not message_data.group_id and not message_data.receiver_id and not message_data.channel_id:
        raise HTTPException(status_code=400, detail="Debe especificar grupo, canal o receptor")
    message = Message(sender_id=sender_id, **message_data.model_dump())
    db.add(message)
    db.commit()
    db.refresh(message)
    return message

@router.get("/group/{group_id}", response_model=List[MessageResponse])
def get_group_messages(group_id: int, db: Session = Depends(get_db)):
    return db.query(Message).filter(Message.group_id == group_id).order_by(Message.created_at).all()

@router.get("/channel/{channel_id}", response_model=List[MessageResponse])
def get_channel_messages(channel_id: int, db: Session = Depends(get_db)):
    return db.query(Message).filter(Message.channel_id == channel_id).order_by(Message.created_at).all()

@router.get("/direct/{user_id}/{other_user_id}", response_model=List[MessageResponse])
def get_direct_messages(user_id: int, other_user_id: int, db: Session = Depends(get_db)):
    return db.query(Message).filter(
        ((Message.sender_id == user_id) & (Message.receiver_id == other_user_id)) |
        ((Message.sender_id == other_user_id) & (Message.receiver_id == user_id))
    ).order_by(Message.created_at).all()

@router.patch("/{message_id}/status", response_model=MessageResponse)
def update_status(message_id: int, status_data: MessageStatusUpdate, db: Session = Depends(get_db)):
    message = db.query(Message).filter(Message.id == message_id).first()
    if not message:
        raise HTTPException(status_code=404, detail="Mensaje no encontrado")
    message.status = status_data.status
    db.commit()
    db.refresh(message)
    return message

@router.get("/{message_id}", response_model=MessageResponse)
def get_message(message_id: int, db: Session = Depends(get_db)):
    message = db.query(Message).filter(Message.id == message_id).first()
    if not message:
        raise HTTPException(status_code=404, detail="Mensaje no encontrado")
    return message

@router.delete("/{message_id}")
def delete_message(message_id: int, db: Session = Depends(get_db)):
    message = db.query(Message).filter(Message.id == message_id).first()
    if not message:
        raise HTTPException(status_code=404, detail="Mensaje no encontrado")
    db.delete(message)
    db.commit()
    return {"message": "Mensaje eliminado"}
