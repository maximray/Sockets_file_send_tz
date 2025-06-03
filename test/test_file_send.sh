#!/bin/bash

set -e

FILE="file_to_send.bin"
FILE_SIZE_MB=2

# 1. Generation file
dd if=/dev/urandom of=$FILE bs=1M count=$FILE_SIZE_MB

# 2. Run server and client
echo "Test server(tcp)"
python3 src/server.py file_to_send.bin &
sleep 1
python3 src/client.py received.bin
wait

# 3. Check equal files
cmp --silent "$FILE" "received.bin" && echo "TCP: OK" || echo "TCP: FAIL"
