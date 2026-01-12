#!/usr/bin/env python3
import sys
from pathlib import Path
from concurrent import futures
import time
import grpc
import configparser

PROTO_DIR = Path(__file__).resolve().parents[1] / "proto"
sys.path.insert(0, str(PROTO_DIR))

import apply_test_pb2
import apply_test_pb2_grpc


class StreamServiceImpl(apply_test_pb2_grpc.StreamServiceServicer):
    def app_func(self, request, context):
        print("app_func")
        base = request.value
        print("  request.value:", base)

        for i in range(10):
            yield apply_test_pb2.BB(value=base + i)
            time.sleep(0.2)

    def app_func2(self, request, context):
        print("app_func2")
        print("  request.i32:", request.i32)
        print("  request.f  :", request.f)
        print("  request.d  :", request.d)
        base = int(request.i32) + int(request.f) + int(request.d)

        for i in range(5):
            yield apply_test_pb2.BB(value=base + i)
            time.sleep(0.2)


def run_server(server_address: str, secure: str):
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))

    apply_test_pb2_grpc.add_StreamServiceServicer_to_server(StreamServiceImpl(), server)

    if secure == "false":
        server.add_insecure_port(server_address)
    else:
        print(f"[WARN] Unsupported secure: {secure} (falling back to false)")
        server.add_insecure_port(server_address)

    server.start()
    print(f"Server listening on {server_address}")
    server.wait_for_termination()


def main():
    server_address = "0.0.0.0:50003"
    secure = "false"

    if len(sys.argv) >= 2:
        ini_file = sys.argv[1]
        config = configparser.ConfigParser()
        try:
            config.read(ini_file)
            server_address = config.get("udf", "endpoint", fallback=server_address)
            secure = config.get("udf", "secure", fallback=secure)
            print(f"[INFO] Loaded gRPC settings from {ini_file}")
        except Exception as e:
            print(f"[WARN] Failed to read ini file '{ini_file}': {e}")
            print("[INFO] Using default gRPC settings")
    else:
        print("[INFO] No ini file specified. Using default gRPC settings")

    run_server(server_address, secure)


if __name__ == "__main__":
    main()
