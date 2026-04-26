import json
import os
import threading
from kafka import KafkaConsumer

KAFKA_BOOTSTRAP_SERVERS = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "kafka:9092")

def consume_presence_events():
    print(">>> [LOG] Intentando conectar a Kafka...")
    try:
        consumer = KafkaConsumer(
            "user-presence",
            bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
            auto_offset_reset="earliest",
            enable_auto_commit=True,
            group_id="user-service-group",
            value_deserializer=lambda v: json.loads(v.decode('utf-8'))
        )
        print(">>> [KAFKA CONECTADO] Escuchando eventos de presencia...")
        for message in consumer:
            print(f"\n[EVENTO RECIBIDO] -> {message.value}")
    except Exception as e:
        print(f"!!! [ERROR KAFKA] No se pudo conectar: {e}")

def start_consumer():
    thread = threading.Thread(target=consume_presence_events, daemon=True)
    thread.start()
    print(">>> [LOG] Hilo de Kafka lanzado en background")
