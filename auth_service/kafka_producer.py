import json
import os
from kafka import KafkaProducer

KAFKA_BOOTSTRAP_SERVERS = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "kafka:9092")

def get_producer():
    return KafkaProducer(
        bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
        value_serializer=lambda v: json.dumps(v).encode('utf-8')
    )

def publish_presence_event(email: str, status: str):
    try:
        producer = get_producer()
        event = {"email": email, "status": status}
        producer.send("user-presence", value=event)
        producer.flush()
        print(f">>> [KAFKA PUBLICADO] {event}")
    except Exception as e:
        print(f"!!! [ERROR KAFKA PRODUCER] {e}")
