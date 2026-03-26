from fastapi import FastAPI
from core.database import get_db
from models.user import Base, UserProfile
from routes import users
from core.database import engine

Base.metadata.create_all(bind=engine)

app = FastAPI(title="User Service", version="1.0.0")

app.include_router(users.router)

@app.get("/health")
def health_check():
    return {"status": "ok", "service": "user-service"}