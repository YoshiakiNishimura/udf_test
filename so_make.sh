#!/usr/bin/env bash

BASE_DIR="${HOME}/grpc"

for item in \
  "apply_test 50003" \
  "load_another 50002" \
  "oneof_test 50001"
do
  set -- $item
  name=$1
  port=$2

  udf-plugin-builder \
    --grpc-endpoint "dns:///localhost:${port}" \
    --proto-file "${name}/proto/${name}.proto" \
    --output-dir "${BASE_DIR}"
done
