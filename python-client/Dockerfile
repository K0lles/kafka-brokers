FROM python:3.13-alpine

# Встановлюємо тільки kafka-python (Faker нам більше не потрібен для CSV)
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

WORKDIR /app
COPY produce.py consume.py run.sh /app/
RUN chmod +x /app/run.sh

ENTRYPOINT ["./run.sh"]
