from fastapi import FastAPI
from core.database import engine
from models.group import Base
from routes import groups
from fastapi.middleware.cors import CORSMiddleware

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Group Service", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(groups.router)

@app.get("/health")
def health_check():
    return {"status": "ok", "service": "group-service"}
