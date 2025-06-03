from socket import *
import sys 
import os
import struct 

BUFFER_SIZE = 65536
PORT = 8080


def run_client(dest_path: str, server_ip: str = "0.0.0.0", port: int = 8080) -> None:
    print(f"requesting from {server_ip}:{port}")
    print("downloading...")
    


    with socket(AF_INET, SOCK_DGRAM) as s:
        s.settimeout(5.0)
        s.sendto(b"GET", (server_ip, port))

        with open(dest_path, "wb") as f:
            expected_id = 0
            while True:
                data, _ = s.recvfrom(BUFFER_SIZE+4)
                if data == b"END":
                    break 

                chunk_id = struct.unpack("!I", data[:4])[0]
                chunk = data[4:]

                if chunk_id == expected_id:
                    f.write(chunk)
                    ack = struct.pack("!I", chunk_id)
                    s.sendto(ack, (server_ip, port))
                    expected_id += 1
                else:
                    # Повторно отправляем ACK на последний полученный
                    if expected_id > 0:
                        ack = struct.pack("!I", expected_id - 1)
                        s.sendto(ack, (server_ip, port))

                
            
    print(f"downloaded as {os.path.abspath(dest_path)}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python client.py <destination_file>")
        sys.exit(1)
    run_client(sys.argv[1])
