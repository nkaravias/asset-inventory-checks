#!/bin/bash
PORT=8090
FUNCTION=pubsub_handler
echo "Starting the functions-framework for ${function} on ${PORT}"
functions-framework --signature-type=cloudevent \
  --source=asset_inventory_checks/main.py \
  --target=$FUNCTION \
  --port=$PORT
