import sys
from pathlib import Path
from concurrent import futures
import grpc

PROTO_DIR = Path(__file__).resolve().parents[1] / "proto"
sys.path.insert(0, str(PROTO_DIR))

import complex_pb2
import complex_pb2_grpc

from tsurugidb.udf import tsurugi_types_pb2


class RecImpl(complex_pb2_grpc.RecServicer):
    def inc_decimal(self, request, context):
        dec = request.value  # tsurugi_types_pb2.Decimal
        print("inc_decimal")
        print("  dec.unscaled_value:", dec.unscaled_value)
        print("  dec.exponent:", dec.exponent)
        unscaled = dec.unscaled_value
        exp = dec.exponent + 1
        return complex_pb2.DecimalMessage(
            value=tsurugi_types_pb2.Decimal(
                unscaled_value=unscaled,
                exponent=exp,
            )
        )


def main():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    complex_pb2_grpc.add_RecServicer_to_server(RecImpl(), server)
    server.add_insecure_port("0.0.0.0:50004")
    server.start()
    print("Server listening on 0.0.0.0:50004")
    server.wait_for_termination()


if __name__ == "__main__":
    main()
