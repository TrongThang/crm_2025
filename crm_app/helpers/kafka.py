from kafka import KafkaProducer, KafkaConsumer
import os
import json
import time

kafka_host = os.getenv('KAFKA_HOST', 'localhost')  # Mặc định là localhost
bootstrap_servers = os.environ.get("KAFKA_BOOTSTRAP_SERVERS", f"{kafka_host}:9092")
# def init_kafka_producer():
#     kafka_host = os.getenv('KAFKA_HOST', 'kafka')
#     bootstrap_servers = f"{kafka_host}:9092"
#     while True:
#         try:
#             producer = KafkaProducer(bootstrap_servers=bootstrap_servers)
#             print("Kafka connected")
#             return producer
#         except Exception as e:
#             print(f"Waiting for Kafka: {e}")
#             time.sleep(1)

producer = KafkaProducer(
    bootstrap_servers=bootstrap_servers,
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

def create_consumer (topic):
    consumer = KafkaConsumer(
        topic,
        bootstrap_servers=bootstrap_servers,
        value_deserializer=lambda m: json.loads(m.decode('utf-8'))
    )

    return consumer