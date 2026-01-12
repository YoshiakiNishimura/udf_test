#!/bin/bash
LIST=(load_another oneof_test apply_test complex)

mkdir -p log
for i in ${LIST[@]}; do
	tgsql -c ipc:tsurugi --script $i/script/test.sql >log/${i}_stdout.log
done
