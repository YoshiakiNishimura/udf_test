#!/bin/bash
udf-plugin-builder --grpc-endpoint dns:///localhost:50002 --proto-file load_another/proto/load_another.proto --output-dir ${HOME}/grpc

udf-plugin-builder --grpc-endpoint dns:///localhost:50001 --proto-file oneof_test/proto/oneof_test.proto --output-dir ${HOME}/grpc
