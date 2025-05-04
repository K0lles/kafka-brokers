import os, json
from kafka import KafkaConsumer

BOOTSTRAP = os.getenv('BOOTSTRAP_SERVERS').split(',')
TOPIC     = os.getenv('TOPIC')
GROUP     = os.getenv('CONSUMER_GROUP')

consumer = KafkaConsumer(
    TOPIC,
    bootstrap_servers=BOOTSTRAP,
    group_id=GROUP,
    auto_offset_reset='earliest',
    value_deserializer=lambda b: json.loads(b.decode())
)

print(f"[*] Consumer {GROUP} listening on {TOPIC}")
for msg in consumer:
    print(f"{GROUP} | {msg.topic}@{msg.partition}/{msg.offset} → {msg.value}")
