from socket import *
import os 
import sys

BUFFER_SIZE = 4096

def send_file(conn: socket, file_path: str) -> None:
    with open(file_path, "rb") as f:
        while chunk := f.read(BUFFER_SIZE):
            conn.sendall(chunk)

def run_server(file_path: str, host: str ="0.0.0.0", port: int = 8080) -> None:
    abs_path = os.path.abspath(file_path)
    print(f"serving {abs_path}")

    with socket(AF_INET, SOCK_STREAM) as s:
        s.bind((host, port))
        s.listen(1)
        conn, addr = s.accept()
        with conn:
            print(f"request from {addr[0]}:{addr[1]}")
            print("sending...")
            send_file(conn, file_path)
            print(f"finished sending to {addr[0]}:{addr[1]}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 server.py <file_to_serve>")
        sys,exit(1)
    run_server(sys.argv[1])
     