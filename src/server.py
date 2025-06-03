from socket import *
import os 
import struct
import sys

BUFFER_SIZE = 4096
ACK_TIMEOUT = 0.5
MAX_RETRIES = 5
PORT = 8080

def run_server(file_path: str, host: str ="0.0.0.0", port: int = 8080) -> None:
    abs_path = os.path.abspath(file_path)
    print(f"serving {abs_path}")

    with socket(AF_INET, SOCK_DGRAM) as s:
        s.bind((host, port))
        
        data, addr = s.recvfrom(65536)
        print(f"request from {addr[0]}:{addr[1]}")
        print("sending...")
            
        with open(file_path, "rb") as f:
            chunk_id = 0
            while True:
                chunk = f.read(BUFFER_SIZE)
                if not chunk:
                    break

                packet = struct.pack("!I", chunk_id) + chunk 
                retries = 0
                while retries < MAX_RETRIES:
                    s.sendto(packet, addr)
                    try:
                        s.settimeout(ACK_TIMEOUT)
                        ack, _ = s.recvfrom(8)
                        ack_id = struct.unpack("!I", ack)[0]
                        if ack_id == chunk_id:
                            break 
                    except timeout:
                        retries += 1
                if retries == MAX_RETRIES:
                    return

                chunk_id += 1

        s.sendto(b"END", addr)
        print(f"finished sending to {addr[0]}:{addr[1]}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 server.py <file_to_serve>")
        sys.exit(1)
    run_server(sys.argv[1])
     