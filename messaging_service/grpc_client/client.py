import grpc
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from grpc_client import auth_pb2, auth_pb2_grpc

AUTH_GRPC_HOST = os.getenv("AUTH_GRPC_HOST", "auth_service")
AUTH_GRPC_PORT = os.getenv("AUTH_GRPC_PORT", "50051")

def validate_token(token: str) -> dict:
    try:
        channel = grpc.insecure_channel(f"{AUTH_GRPC_HOST}:{AUTH_GRPC_PORT}")
        stub = auth_pb2_grpc.AuthServiceStub(channel)
        response = stub.ValidateToken(auth_pb2.TokenRequest(token=token))
        return {
            "is_valid": response.is_valid,
            "email": response.email,
            "user_id": response.user_id,
            "message": response.message
        }
    except Exception as e:
        return {
            "is_valid": False,
            "email": "",
            "user_id": 0,
            "message": f"Error conectando con auth_service: {str(e)}"
        }
