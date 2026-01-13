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

    def stream_decimal(self, request, context):
        dec = request.value
        print("stream_decimal")
        print("  start:", dec.unscaled_value, dec.exponent)

        unscaled = dec.unscaled_value
        exp = dec.exponent

        for i in range(5):
            yield complex_pb2.DecimalMessage(
                value=tsurugi_types_pb2.Decimal(
                    unscaled_value=unscaled,
                    exponent=exp + i,
                )
            )

    def inc_two(self, request, context):
        # request: TwoMessage { date, lt }
        d = request.date  # tsurugi_types_pb2.Date (days)
        lt = request.lt  # tsurugi_types_pb2.LocalTime (nanos)

        print("inc_two")
        print("  date.days:", d.days)
        print("  lt.nanos:", lt.nanos)

        return complex_pb2.DataMessage(date=tsurugi_types_pb2.Date(days=d.days + 1))

    def stream_two(self, request, context):
        d = request.date
        lt = request.lt

        print("stream_two")
        print("  date.days:", d.days)
        print("  lt.nanos:", lt.nanos)

        for i in range(5):
            if not context.is_active():
                print("  client disconnected")
                break
            yield complex_pb2.DataMessage(date=tsurugi_types_pb2.Date(days=d.days + i))

    def inc_another_two(self, request, context):
        ld = request.ldt
        od = request.odt

        print("inc_another_two")
        print("  ld.offset_seconds:", ld.offset_seconds)
        print("  ld.nano_adjustment:", ld.nano_adjustment)
        print("  od.offset_seconds:", od.offset_seconds)
        print("  od.nano_adjustment:", od.nano_adjustment)
        print("  od.time_zone_offset:", od.time_zone_offset)

        return complex_pb2.OffsetDatetimeMessage(
            odt=tsurugi_types_pb2.OffsetDatetime(
                offset_seconds=od.offset_seconds,
                nano_adjustment=od.nano_adjustment,
                time_zone_offset=od.time_zone_offset,
            )
        )

    def stream_another_two(self, request, context):
        ld = request.ldt
        od = request.odt

        print("stream_another_two")
        print("  ld.offset_seconds:", ld.offset_seconds)
        print("  ld.nano_adjustment:", ld.nano_adjustment)
        print("  od.offset_seconds:", od.offset_seconds)
        print("  od.nano_adjustment:", od.nano_adjustment)
        print("  od.time_zone_offset:", od.time_zone_offset)

        for i in range(5):
            if not context.is_active():
                print("  client disconnected")
                break
            yield complex_pb2.OffsetDatetimeMessage(
                odt=tsurugi_types_pb2.OffsetDatetime(
                    offset_seconds=od.offset_seconds,
                    nano_adjustment=od.nano_adjustment,
                    time_zone_offset=od.time_zone_offset,
                )
            )

    def inc_alltypes(self, request, context):
        print("inc_alltypes")
        self._print_alltypes_request(request)

        b = request.blob
        out_blob = tsurugi_types_pb2.BlobReference(
            storage_id=b.storage_id,
            object_id=b.object_id,
            tag=b.tag + 1,
            provisioned=b.provisioned,
        )
        return complex_pb2.BlobMessage(blob=out_blob)

    # --- new: server streaming ---
    def stream_alltypes(self, request, context):
        print("stream_alltypes")
        self._print_alltypes_request(request)

        b = request.blob
        for i in range(5):
            if not context.is_active():
                print("  client disconnected")
                break

            out_blob = tsurugi_types_pb2.BlobReference(
                storage_id=b.storage_id,
                object_id=b.object_id,
                tag=b.tag,
                provisioned=b.provisioned,
            )
            yield complex_pb2.BlobMessage(blob=out_blob)

    def inc_blob(self, request, context):
        bl = request.blob
        print("inc_blob")
        print("  blob strage_id", bl.storage_id)
        print("  blob object_id", bl.object_id)
        print("  blob tag", bl.tag)
        print("  blob provisioned", bl.provisioned)

        out_ref = tsurugi_types_pb2.BlobReference(
            storage_id=bl.storage_id,
            object_id=bl.object_id,
            tag=bl.tag,
            provisioned=bl.provisioned,
        )
        return complex_pb2.BlobMessage(blob=out_ref)

    def stream_blob(self, request, context):
        bl = request.blob
        print("stream_blob")
        print("  blob strage_id", bl.storage_id)
        print("  blob object_id", bl.object_id)
        print("  blob tag", bl.tag)
        print("  blob provisioned", bl.provisioned)

        out_ref = tsurugi_types_pb2.BlobReference(
            storage_id=bl.storage_id,
            object_id=bl.object_id,
            tag=bl.tag,
            provisioned=bl.provisioned,
        )
        for i in range(5):
            if not context.is_active():
                print("  client disconnected")
                break
            yield complex_pb2.BlobMessage(blob=out_ref)

    def inc_three(self, request, context):
        bl = request.blob
        cl = request.clob
        ldt = request.ldt
        print("inc_three")
        print("  blob strage_id", bl.storage_id)
        print("  blob object_id", bl.object_id)
        print("  clob strage_id", cl.storage_id)
        print("  clob object_id", cl.object_id)
        print("  ldt.offset_seconds:", ldt.offset_seconds)
        print("  ldt.nano_adjustment:", ldt.nano_adjustment)

        return complex_pb2.BlobMessage(blob=bl)

    def stream_three(self, request, context):
        bl = request.blob
        cl = request.clob
        ldt = request.ldt
        print("stream_three")
        print("  blob strage_id", bl.storage_id)
        print("  blob object_id", bl.object_id)
        print("  clob strage_id", cl.storage_id)
        print("  clob object_id", cl.object_id)
        print("  ldt.offset_seconds:", ldt.offset_seconds)
        print("  ldt.nano_adjustment:", ldt.nano_adjustment)

        for i in range(5):
            if not context.is_active():
                print("  client disconnected")
                break
            yield complex_pb2.BlobMessage(blob=bl)

    @staticmethod
    def _print_alltypes_request(req):
        # Decimal
        print("  dec.unscaled_value:", req.dec.unscaled_value)
        print("  dec.exponent:", req.dec.exponent)

        # Date
        print("  date.days:", req.date.days)

        # LocalTime
        print("  lt.nanos:", req.lt.nanos)

        # LocalDatetime
        print("  ldt.offset_seconds:", req.ldt.offset_seconds)
        print("  ldt.nano_adjustment:", req.ldt.nano_adjustment)

        # OffsetDatetime
        print("  odt.offset_seconds:", req.odt.offset_seconds)
        print("  odt.nano_adjustment:", req.odt.nano_adjustment)
        print("  odt.time_zone_offset:", req.odt.time_zone_offset)

        # BlobReference / ClobReference
        print("  blob.storage_id:", req.blob.storage_id)
        print("  blob.object_id:", req.blob.object_id)
        print("  blob.tag:", req.blob.tag)
        print("  blob.provisioned:", req.blob.provisioned)

        print("  clob.storage_id:", req.clob.storage_id)
        print("  clob.object_id:", req.clob.object_id)
        print("  clob.tag:", req.clob.tag)
        print("  clob.provisioned:", req.clob.provisioned)


def main():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    complex_pb2_grpc.add_RecServicer_to_server(RecImpl(), server)
    server.add_insecure_port("0.0.0.0:50004")
    server.start()
    print("Server listening on 0.0.0.0:50004")
    server.wait_for_termination()


if __name__ == "__main__":
    main()
