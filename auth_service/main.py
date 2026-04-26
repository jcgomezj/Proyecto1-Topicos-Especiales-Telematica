import threading
from fastapi import FastAPI
from core.database import engine
from models.user import Base
from routes import auth
from fastapi.middleware.cors import CORSMiddleware

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Auth Service", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)

@app.on_event("startup")
def startup_grpc():
    from grpc_server.server import serve
    thread = threading.Thread(target=serve, daemon=True)
    thread.start()
    print("gRPC server iniciado en hilo separado")

@app.get("/health")
def health_check():
    return {"status": "ok", "service": "auth-service", "grpc_port": 50051}
