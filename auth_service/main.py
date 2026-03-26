from fastapi import FastAPI
from core.database import engine
from models.user import Base
from routes import auth

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Auth Service", version="1.0.0")

app.include_router(auth.router)

@app.get("/health")
def health_check():
    return {"status": "ok", "service": "auth-service"}