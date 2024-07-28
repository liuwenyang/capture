import socket
import threading

start_save_flag = threading.Event()

class SocketServer:
    def __init__(self, ip='127.0.0.1', port=12345):
        self.ip = ip
        self.port = port
        self.server_socket = None

    def __enter__(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.server_socket.bind((self.ip, self.port))
        print(f"Listening on {self.ip}:{self.port}")
        return self.server_socket

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.server_socket:
            self.server_socket.close()
            print("Server socket closed.")

def listen_for_signal(ip='127.0.0.1', port=12345, signal='0001'):
    """监听特定信号来更改全局标志位"""
    with SocketServer(ip, port) as server_socket:
        try:
            while True:
                data, _ = server_socket.recvfrom(1024)
                if data.decode() == signal:
                    print(f'收到信号: {data.decode()}')
                    start_save_flag.set()
                    print(f"start_save_flag状态:{start_save_flag}")
        except KeyboardInterrupt:
            print("Server interrupted by user.")
        except Exception as e:
            print(f"An error occurred: {e}")
        finally:
            start_save_flag.clear()
            print(f"start_save_flag状态:{start_save_flag}")

if __name__ == '__main__':
    try:
        listen_for_signal()
    except Exception as e:
        print(f"Unexpected error: {e}")
