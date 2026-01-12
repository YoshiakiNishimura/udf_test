#!/usr/bin/env bash
set -euo pipefail
TSURUGI_PROTO_DIR=${HOME}/git/tsurugi-udf/proto
BASE_DIR="$(cd "$(dirname "$0")" && pwd)"
PYTHON=python3

#  "load_another"
#  "oneof_test"
#  "apply_test"
TESTS=(
	"complex"
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

	if [[ "$test" == "complex" ]]; then
		${PYTHON} -m grpc_tools.protoc \
			-I "${PROTO_DIR}" \
			-I "${TSURUGI_PROTO_DIR}" \
			--python_out="${PROTO_DIR}" \
			--grpc_python_out="${PROTO_DIR}" \
			"${PROTO_DIR}/complex.proto"

		GENERATED_FILES+=(
			"${PROTO_DIR}/complex_pb2.py"
			"${PROTO_DIR}/complex_pb2_grpc.py"
		)
	else
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
	fi
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
