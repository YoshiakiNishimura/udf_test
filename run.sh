#!/usr/bin/env bash
set -euo pipefail

BASE_DIR="$(cd "$(dirname "$0")" && pwd)"
PYTHON=python3

TESTS=(
  "load_another"
  "oneof_test"
  "apply_test"
)

GENERATED_FILES=()
SERVER_PIDS=()

cleanup() {
    echo "[INFO] Cleaning up..."

    for pid in "${SERVER_PIDS[@]}"; do
        if kill -0 "$pid" 2>/dev/null; then
            echo "[INFO] Stopping server pid=$pid"
            kill "$pid"
            wait "$pid" 2>/dev/null || true
        fi
    done

    for f in "${GENERATED_FILES[@]}"; do
        if [[ -f "$f" ]]; then
            echo "[INFO] Removing generated file: $f"
            rm -f "$f"
        fi
    done
}

trap cleanup EXIT INT TERM

for test in "${TESTS[@]}"; do
    PROTO_DIR="${BASE_DIR}/${test}/proto"

    echo "[INFO] Generating Python gRPC code for ${test}..."

    cd "${PROTO_DIR}"
    for proto in *.proto; do
        ${PYTHON} -m grpc_tools.protoc \
          -I. \
          --python_out=. \
          --grpc_python_out=. \
          "$proto"

        base="${proto%.proto}"
        GENERATED_FILES+=(
          "${PROTO_DIR}/${base}_pb2.py"
          "${PROTO_DIR}/${base}_pb2_grpc.py"
        )
    done
done

echo "[INFO] Proto code generated"

for test in "${TESTS[@]}"; do
    SERVER_DIR="${BASE_DIR}/${test}/server"
    echo "[INFO] Starting gRPC server: ${test}"

    (
      cd "${SERVER_DIR}"
      ${PYTHON} rpc_server.py
    ) &

    SERVER_PIDS+=("$!")
done

echo "[INFO] All gRPC servers started"
echo "[INFO] Press Ctrl+C to stop"

wait

