import csv, json, os, time
from kafka import KafkaProducer

BOOTSTRAP = os.getenv('BOOTSTRAP_SERVERS').split(',')
TOPICS    = os.getenv('TOPICS', '').split(',')
CSV_PATH  = os.getenv('CSV_PATH')

producer = KafkaProducer(
    bootstrap_servers=BOOTSTRAP,
    value_serializer=lambda v: json.dumps(v).encode()
)

with open(CSV_PATH, newline='') as f:
    reader = csv.DictReader(f)
    for row in reader:
        # row — вже dict(str: str).
        for topic in TOPICS:
            producer.send(topic, row)
            print(f"sent to {topic}: {row}")
        time.sleep(1)  # щоб не штурмувати кластер
