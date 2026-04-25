from fastapi import FastAPI
from core.database import engine
from models.message import Base
from routes import messages
from fastapi.middleware.cors import CORSMiddleware

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Messaging Service", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(messages.router)

@app.get("/health")
def health_check():
    return {"status": "ok", "service": "messaging-service"}
