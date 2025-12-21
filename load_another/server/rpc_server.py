import sys
from pathlib import Path

# add proto directory to sys.path
PROTO_DIR = Path(__file__).resolve().parents[1] / "proto"
sys.path.insert(0, str(PROTO_DIR))

import grpc
from concurrent import futures
import configparser

import load_another_pb2
import load_another_pb2_grpc

class GreeterServiceImpl(load_another_pb2_grpc.GreeterServicer):

    def SayHello(self, request, context):
        prefix = "Hello "
        print("SayHello")
        print("  prefix:", prefix)
        print("  request.value:", request.value)
        return load_another_pb2.StringValue(value=prefix + request.value)

    def IntAddInt(self, request, context):
        print("IntAddInt")
        print("  request.value:", request.value)
        return load_another_pb2.Int32Value(value=request.value + 1)

    def EmptyReq(self, request, context):
        print("EmptyReq")
        return load_another_pb2.Int32Value(value=111)


class ByerServiceImpl(load_another_pb2_grpc.ByerServicer):

    def SayWorld(self, request, context):
        prefix = "World "
        print("SayWorld")
        print("  prefix:", prefix)
        print("  request.value:", request.value)
        return load_another_pb2.StringValue(value=prefix + request.value)


def run_server(server_address: str, secure: str):
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))

    load_another_pb2_grpc.add_GreeterServicer_to_server(
        GreeterServiceImpl(), server
    )
    load_another_pb2_grpc.add_ByerServicer_to_server(
        ByerServiceImpl(), server
    )

    if secure == "false":
        server.add_insecure_port(server_address)
    else:
        print(f"[WARN] Unsupported secure: {secure} (falling back to false)")
        server.add_insecure_port(server_address)

    server.start()
    print(f"Server listening on {server_address}")
    server.wait_for_termination()


def main():
    server_address = "0.0.0.0:50002"
    secure = "false"

    if len(sys.argv) >= 2:
        ini_file = sys.argv[1]
        config = configparser.ConfigParser()
        try:
            config.read(ini_file)
            server_address = config.get(
                "udf", "endpoint", fallback=server_address
            )
            secure = config.get(
                "udf", "secure", fallback=secure
            )
            print(f"[INFO] Loaded gRPC settings from {ini_file}")
        except Exception as e:
            print(f"[WARN] Failed to read ini file '{ini_file}': {e}")
            print("[INFO] Using default gRPC settings")
    else:
        print("[INFO] No ini file specified. Using default gRPC settings")

    run_server(server_address, secure)


if __name__ == "__main__":
    main()

