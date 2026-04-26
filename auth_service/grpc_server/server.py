import grpc
from concurrent import futures
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from grpc_server import auth_pb2, auth_pb2_grpc
from core.security import decode_token
from core.database import SessionLocal
from models.user import User

class AuthServicer(auth_pb2_grpc.AuthServiceServicer):
    def ValidateToken(self, request, context):
        email = decode_token(request.token)
        if not email:
            return auth_pb2.TokenResponse(
                is_valid=False,
                email="",
                user_id=0,
                message="Token invalido o expirado"
            )
        db = SessionLocal()
        try:
            user = db.query(User).filter(User.email == email).first()
            if not user or not user.is_active:
                return auth_pb2.TokenResponse(
                    is_valid=False,
                    email="",
                    user_id=0,
                    message="Usuario no encontrado o inactivo"
                )
            return auth_pb2.TokenResponse(
                is_valid=True,
                email=email,
                user_id=user.id,
                message="Token valido"
            )
        finally:
            db.close()

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    auth_pb2_grpc.add_AuthServiceServicer_to_server(AuthServicer(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    print("gRPC server corriendo en puerto 50051")
    server.wait_for_termination()

if __name__ == '__main__':
    serve()
