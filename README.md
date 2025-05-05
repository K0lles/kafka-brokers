## Запуск стеку
Клонування репозиторію:
```bash
   git clone ...
   cd <repo>/docker/kafka-brokers
   ```
Помістіть ваш CSV у папку csv-data з імʼям data.csv.

```bash
  # Підніміть контейнери:
    docker compose up -d --build
```

Створення топіків
За замовчуванням брокери слухають на портах 29091–29093 у внутрішній мережі Docker.

```bash
  # Створити Topic1
  docker exec broker-1 kafka-topics \
    --create --bootstrap-server broker-1:29091 \
    --topic Topic1 --partitions 1 --replication-factor 1 \
    --if-not-exists
```

```bash
  # Створити Topic2
  docker exec broker-1 kafka-topics \
    --create --bootstrap-server broker-1:29091 \
    --topic Topic2 --partitions 1 --replication-factor 1 \
    --if-not-exists
```
Перевірка роботи.
Для реального часу логів виконайте:

```bash
  docker compose logs -f producer consumer1 consumer2
```
У виводі має бути:

```bash
  producer    | sent to Topic1: {...}
  producer    | sent to Topic2: {...}
  consumer1   | Topic1@0/0 → {...}
  consumer2   | Topic2@0/0 → {...}
```
