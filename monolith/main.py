from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from monolith.database import engine
from monolith.models.user import Base as UserBase
from monolith.models.group import Group, GroupMember, Channel
from monolith.models.message import Message, File
from monolith.routes import auth, users, groups, messages
from fastapi.middleware.cors import CORSMiddleware

UserBase.metadata.create_all(bind=engine)

app = FastAPI(title="GroupsApp", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(groups.router)
app.include_router(messages.router)

app.mount("/static", StaticFiles(directory="monolith/static"), name="static")

@app.get("/")
def root():
    return FileResponse("monolith/static/index.html")

@app.get("/health")
def health_check():
    return {"status": "ok", "service": "groupsapp-monolith"}
