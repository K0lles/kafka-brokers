import os
import csv
import json
from datetime import datetime
from io import TextIOWrapper

from kafka import KafkaConsumer
from minio import Minio
from minio.error import S3Error

# Kafka налаштування
BOOTSTRAP = os.getenv('BOOTSTRAP_SERVERS').split(',')
TOPIC = os.getenv('TOPIC')
GROUP = os.getenv('CONSUMER_GROUP')

# Minio налаштування
MINIO_ENDPOINT = os.getenv('MINIO_ENDPOINT')
MINIO_ACCESS_KEY = os.getenv('MINIO_ROOT_USER')
MINIO_SECRET_KEY = os.getenv('MINIO_ROOT_PASSWORD')
MINIO_BUCKET = os.getenv('MINIO_BUCKET')

# Підключаємося до Kafka
consumer = KafkaConsumer(
    TOPIC,
    bootstrap_servers=BOOTSTRAP,
    group_id=GROUP,
    auto_offset_reset='earliest',
    value_deserializer=lambda b: json.loads(b.decode('utf-8'))
)

# Підключаємося до Minio
minio_client = Minio(
    MINIO_ENDPOINT,
    access_key=MINIO_ACCESS_KEY,
    secret_key=MINIO_SECRET_KEY,
    secure=False
)
if not minio_client.bucket_exists(MINIO_BUCKET):
    minio_client.make_bucket(MINIO_BUCKET)

current_month_id = None
current_file: TextIOWrapper | None = None
csv_writer = None

def rotate_file(new_month_id):
    global current_month_id, current_file, csv_writer

    # закриваємо й аплоадимо попередній файл
    if current_file:
        current_file.close()
        prev_name = f"{current_month_id}.csv"
        try:
            minio_client.fput_object(
                MINIO_BUCKET,
                prev_name,
                prev_name
            )
            os.remove(prev_name)
            print(f"Uploaded & removed {prev_name}")
        except S3Error as err:
            print(f"Upload error for {prev_name}: {err}")

    # готуємо новий файл
    current_month_id = new_month_id
    current_file = open(f"{new_month_id}.csv", 'w', newline='')
    csv_writer = None  # створимо нижче при отриманні першого рядка

for msg in consumer:
    record = msg.value
    # парсимо дату з повідомлення
    dt = datetime.fromisoformat(record['start_time'])
    month_str = dt.strftime('%B').lower()
    new_id    = f"{month_str}_{dt.year}"

    if new_id != current_month_id:
        rotate_file(new_id)

    # як тільки csv_writer ще не створено — ініціалізуємо его з заголовками
    if csv_writer is None:
        fieldnames = list(record.keys())
        csv_writer = csv.DictWriter(current_file, fieldnames=fieldnames)
        csv_writer.writeheader()

    # пишемо рядок
    csv_writer.writerow(record)
    current_file.flush()
