from socket import *
import sys 
import os

BUFFER_SIZE = 4096

def receive_file(s: socket, dest_path: str) -> None:
    with open(dest_path, "wb") as f:
        while chunk := s.recv(BUFFER_SIZE):
            if not chunk:
                break
            f.write(chunk)

def run_client(dest_path: str, server_ip: str = "0.0.0.0", port: int = 8080) -> None:
    print(f"requesting from {server_ip}:{port}")
    print("downloading...")
    
    with socket(AF_INET, SOCK_STREAM) as s:
        s.connect((server_ip, port))
        receive_file(s, dest_path)

    print(f"downloaded as {os.path.abspath(dest_path)}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python client.py <destination_file>")
        sys.exit(1)
    run_client(sys.argv[1])
