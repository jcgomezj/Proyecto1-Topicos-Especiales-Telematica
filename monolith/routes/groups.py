from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from monolith.database import get_db
from monolith.models.group import Group, GroupMember, Channel
from monolith.schemas.group import GroupCreate, GroupResponse, GroupMemberCreate, GroupMemberResponse, ChannelCreate, ChannelResponse

router = APIRouter(prefix="/groups", tags=["groups"])

@router.post("/", response_model=GroupResponse, status_code=201)
def create_group(group_data: GroupCreate, created_by: int, db: Session = Depends(get_db)):
    group = Group(**group_data.model_dump(), created_by=created_by)
    db.add(group)
    db.commit()
    db.refresh(group)
    member = GroupMember(group_id=group.id, user_id=created_by, role="admin")
    db.add(member)
    db.commit()
    return group

@router.get("/", response_model=List[GroupResponse])
def get_groups(db: Session = Depends(get_db)):
    return db.query(Group).all()

@router.get("/{group_id}", response_model=GroupResponse)
def get_group(group_id: int, db: Session = Depends(get_db)):
    group = db.query(Group).filter(Group.id == group_id).first()
    if not group:
        raise HTTPException(status_code=404, detail="Grupo no encontrado")
    return group

@router.post("/{group_id}/members", response_model=GroupMemberResponse, status_code=201)
def add_member(group_id: int, member_data: GroupMemberCreate, db: Session = Depends(get_db)):
    group = db.query(Group).filter(Group.id == group_id).first()
    if not group:
        raise HTTPException(status_code=404, detail="Grupo no encontrado")
    member = GroupMember(group_id=group_id, **member_data.model_dump())
    db.add(member)
    db.commit()
    db.refresh(member)
    return member

@router.get("/{group_id}/members", response_model=List[GroupMemberResponse])
def get_members(group_id: int, db: Session = Depends(get_db)):
    return db.query(GroupMember).filter(GroupMember.group_id == group_id).all()

@router.post("/{group_id}/channels", response_model=ChannelResponse, status_code=201)
def create_channel(group_id: int, channel_data: ChannelCreate, db: Session = Depends(get_db)):
    group = db.query(Group).filter(Group.id == group_id).first()
    if not group:
        raise HTTPException(status_code=404, detail="Grupo no encontrado")
    channel = Channel(group_id=group_id, **channel_data.model_dump())
    db.add(channel)
    db.commit()
    db.refresh(channel)
    return channel

@router.get("/{group_id}/channels", response_model=List[ChannelResponse])
def get_channels(group_id: int, db: Session = Depends(get_db)):
    return db.query(Channel).filter(Channel.group_id == group_id).all()
