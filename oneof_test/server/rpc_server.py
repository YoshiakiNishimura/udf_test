#!/usr/bin/env python3
import sys
from pathlib import Path
from concurrent import futures
import grpc
import configparser

PROTO_DIR = Path(__file__).resolve().parents[1] / "proto"
sys.path.insert(0, str(PROTO_DIR))

import oneof_test_pb2
import oneof_test_pb2_grpc


class OneService(oneof_test_pb2_grpc.OneServicer):

    def OneofAlpha(self, request, context):
        print("OneofAlpha")
        print("a :", request.a)
        return oneof_test_pb2.Mm(a=64 + request.a)

    def OneofBeta(self, request, context):
        print("OneofBeta")

        print("int64_result :", request.int64_result)
        print("string_result :", request.string_result)

        return oneof_test_pb2.Mm(a=64 + request.int64_result)

    def EchoOneOf(self, request, context):
        print("EchoOneOf")
        prefix = "Hello "

        print("  prefix:", prefix)
        print("  request.aaa:", request.aaa)
        print("  request.bbb:", request.bbb)

        arg_case = request.WhichOneof("arg")
        print("  oneof arg case:", arg_case)

        if arg_case == "int64_value":
            print("  int64_value:", request.int64_value)
        elif arg_case == "string_value":
            print("  string_value:", request.string_value)
        elif arg_case == "bool_value":
            print("  bool_value:", request.bool_value)
        else:
            print("  oneof (arg) not set")

        aab_case = request.WhichOneof("aab")
        print("  oneof aab case:", aab_case)

        if aab_case == "int64_value2":
            print("  int64_value2:", request.int64_value2)
        elif aab_case == "string_value2":
            print("  string_value2:", request.string_value2)
        elif aab_case == "bool_value2":
            print("  bool_value2:", request.bool_value2)
        else:
            print("  oneof (aab) not set")

        parts = [prefix, str(request.aaa)]

        if arg_case == "int64_value":
            parts.append(str(request.int64_value))
        elif arg_case == "string_value":
            parts.append(request.string_value)
        elif arg_case == "bool_value":
            parts.append("true" if request.bool_value else "false")

        if aab_case == "int64_value2":
            parts.append(str(request.int64_value2))
        elif aab_case == "string_value2":
            parts.append(request.string_value2)
        elif aab_case == "bool_value2":
            parts.append("true" if request.bool_value2 else "false")

        result = "".join(parts)
        return oneof_test_pb2.MyReply(string_result=result)


def run_server(ini_path=None):
    server_address = "0.0.0.0:50001"
    secure = "false"

    if ini_path:
        config = configparser.ConfigParser()
        try:
            config.read(ini_path)
            server_address = config.get("udf", "endpoint", fallback=server_address)
            secure = config.get("udf", "secure", fallback=secure)
            print(f"[INFO] Loaded gRPC settings from {ini_path}")
        except Exception as e:
            print(f"[WARN] Failed to read ini file '{ini_path}': {e}")
            print("[INFO] Using default gRPC settings")
    else:
        print("[INFO] No ini file specified. Using default gRPC settings")

    server = grpc.server(futures.ThreadPoolExecutor(max_workers=4))
    oneof_test_pb2_grpc.add_OneServicer_to_server(OneService(), server)

    if secure == "false":
        server.add_insecure_port(server_address)
    else:
        print(f"[WARN] Unsupported secure: {secure} (falling back to false)")
        server.add_insecure_port(server_address)

    server.start()
    print("Server listening on", server_address)
    server.wait_for_termination()


if __name__ == "__main__":
    ini_file = sys.argv[1] if len(sys.argv) >= 2 else None
    run_server(ini_file)

