import csv, json, os, time
from datetime import datetime

from kafka import KafkaProducer

BOOTSTRAP = os.getenv('BOOTSTRAP_SERVERS').split(',')
TOPICS    = os.getenv('TOPICS', '').split(',')
CSV_PATH  = os.getenv('CSV_PATH')
# Зчитуємо весь CSV і сортуємо за датою (поле start_time)
with open(CSV_PATH, newline='') as f:
    reader = csv.DictReader(f)
    rows = list(reader)

rows.sort(key=lambda r: datetime.fromisoformat(r['start_time']))

producer = KafkaProducer(
    bootstrap_servers=BOOTSTRAP,
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

for row in rows:
    for topic in TOPICS:
        producer.send(topic, row)
        print(f"sent to {topic}: {row}")

producer.flush()
producer.close()