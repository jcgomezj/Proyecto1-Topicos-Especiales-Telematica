from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Enum
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class Message(Base):
    __tablename__ = "messages"
    id = Column(Integer, primary_key=True, index=True)
    sender_id = Column(Integer, nullable=False)
    group_id = Column(Integer, nullable=True)
    channel_id = Column(Integer, nullable=True)
    receiver_id = Column(Integer, nullable=True)
    content = Column(String, nullable=True)
    message_type = Column(Enum("text", "file", "image", name="message_type"), default="text")
    status = Column(Enum("sent", "delivered", "read", name="message_status"), default="sent")
    created_at = Column(DateTime, default=datetime.utcnow)

class File(Base):
    __tablename__ = "files"
    id = Column(Integer, primary_key=True, index=True)
    message_id = Column(Integer, ForeignKey("messages.id"), nullable=False)
    filename = Column(String, nullable=False)
    file_url = Column(String, nullable=False)
    file_size = Column(Integer, nullable=True)
    file_type = Column(String, nullable=True)
    uploaded_at = Column(DateTime, default=datetime.utcnow)
