#!/usr/bin/env sh
set -e

if [ "$ACTION" = "producer" ]; then
  echo "[run.sh] starting producer"
  python3 produce.py

elif [ "$ACTION" = "consumer" ]; then
  echo "[run.sh] starting consumer"
  python3 consume.py

else
  echo "[run.sh] unknown ACTION=$ACTION"
  exec /bin/sh
fi
