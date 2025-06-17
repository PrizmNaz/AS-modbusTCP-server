import socket
import argparse
import sys
import time

def tcp_client(host: str, port: int):
    """
    Simple TCP/IP client that connects to the specified host and port,
    keeps retrying until connection succeeds, sends user-entered strings,
    receives responses, and closes on 'close' command.
    """
    # Retry loop for connection
    while True:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect((host, port))
            print(f"Connected to {host}:{port}")
            break
        except Exception as e:
            print(f"Connection to {host}:{port} failed: {e}. Retrying in 5 seconds...")
            time.sleep(5)

    with sock:
        while True:
            try:
                message = input('Enter message (type "close" to exit): ')
            except EOFError:
                print("\nEOF detected, closing connection.")
                break

            sock.sendall(message.encode())

            if message.lower() == 'close':
                print("Close command sent. Closing connection.")
                break

            data = sock.recv(4096)
            if not data:
                print("Server closed the connection.")
                break
            print(f"Received: {data.decode()}")

def main():
    parser = argparse.ArgumentParser(description='Simple TCP/IP client')
    parser.add_argument('host', help='IP address or hostname of the server')
    parser.add_argument('port', type=int, help='Port number of the server')
    args = parser.parse_args()

    tcp_client(args.host, args.port)

if __name__ == '__main__':
    main()