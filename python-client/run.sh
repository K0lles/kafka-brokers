#!/usr/bin/env sh
set -x

if [ "$ACTION" == "producer" ]
then
  echo "starting $ACTION"
  env | grep BOOTSTRAP
  python3 produce.py
fi

if [ "$ACTION" == "consumer" ]
then
  echo "starting $ACTION"
  env | grep BOOTSTRAP
  python3 consume.py
fi

if [ "$ACTION" == "shell" ]
then
  sleep 10000000
fi
