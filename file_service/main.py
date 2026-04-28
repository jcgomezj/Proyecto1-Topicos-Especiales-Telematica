from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import StreamingResponse
from minio import Minio
from minio.error import S3Error
import os

app = FastAPI(title="File Service", version="1.0.0")

MINIO_ENDPOINT = os.getenv("MINIO_ENDPOINT", "minio:9000")
MINIO_ACCESS_KEY = os.getenv("MINIO_ACCESS_KEY", "minioadmin")
MINIO_SECRET_KEY = os.getenv("MINIO_SECRET_KEY", "minioadmin")
MINIO_BUCKET = os.getenv("MINIO_BUCKET", "files")

minio_client = Minio(
    MINIO_ENDPOINT,
    access_key=MINIO_ACCESS_KEY,
    secret_key=MINIO_SECRET_KEY,
    secure=False
)

@app.on_event("startup")
def startup_event():
    try:
        found = minio_client.bucket_exists(MINIO_BUCKET)
        if not found:
            minio_client.make_bucket(MINIO_BUCKET)
            print(f"Bucket '{MINIO_BUCKET}' creado")
    except Exception as e:
        print(f"Error al inicializar MinIO: {e}")

@app.get("/health")
def health_check():
    return {"status": "ok", "service": "file-service"}

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    try:
        minio_client.put_object(
            MINIO_BUCKET,
            file.filename,
            file.file,
            length=-1,
            part_size=10*1024*1024,
        )
        return {"filename": file.filename, "status": "uploaded"}
    except S3Error as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/download/{filename}")
def download_file(filename: str):
    try:
        response = minio_client.get_object(MINIO_BUCKET, filename)
        return StreamingResponse(
            response.stream(),
            media_type="application/octet-stream",
            headers={"Content-Disposition": f"attachment; filename={filename}"}
        )
    except S3Error:
        raise HTTPException(status_code=404, detail="File not found")

@app.delete("/files/{filename}")
def delete_file(filename: str):
    try:
        minio_client.remove_object(MINIO_BUCKET, filename)
        return {"filename": filename, "status": "deleted"}
    except S3Error:
        raise HTTPException(status_code=404, detail="File not found")