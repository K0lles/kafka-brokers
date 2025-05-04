**docker compose up -d --build**

**docker exec broker-1 kafka-topics \
  --create --bootstrap-server broker-1:29091 \
  --topic Topic1 --partitions 1 --replication-factor 1 --if-not-exists**

**docker exec broker-1 kafka-topics \
  --create --bootstrap-server broker-1:29091 \
  --topic Topic2 --partitions 1 --replication-factor 1 --if-not-exists**
