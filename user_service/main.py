from fastapi import FastAPI
import kafka_consumer

app = FastAPI()

@app.on_event("startup")
async def startup_event():
    print("\n" + "="*50)
    print(" INICIANDO USER_SERVICE Y KAFKA ")
    print("="*50 + "\n")
    kafka_consumer.start_consumer()

@app.get("/")
async def root():
    return {"status": "User Service is running"}
