import socket
from log import Log
from action import action1

class SocketServer:
    def __init__(self, ip='0.0.0.0', port=12345):
        self.ip = ip
        self.port = port
        self.server_socket = None

    def __enter__(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.server_socket.bind((self.ip, self.port))
        Log.info(f"Server listening on {self.server_socket.getsockname()[0]}:{self.port}")


        return self.server_socket

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.server_socket:
            self.server_socket.close()
            print("Server socket closed.")

def listen_for_signal(ip='0.0.0.0', port=12345, signal='0001'):
    from main import event
    from config_loader import config
    with SocketServer(ip, port) as server_socket:
        try:
            while True:
                try:
                    data, _ = server_socket.recvfrom(1024)
                    if data.decode() == signal:
                        Log.debug(f"收到来自{ip}:{port}的信号: {data.decode()}")
                        # 回复发送方相同信号+1
                        server_socket.sendto(str(int(signal) + 1).encode(), (_))
                        Log.debug(f"回复来自{ip}:{port}的信号: {str(int(signal) + 1)}")
                        action1()
                        Log.debug(f"流程进入后 event.output_folder_path:{event.output_folder_path}, event.usage_count: {event.usage_count}")
                except Exception as inner_e:
                    print(f"An error occurred inside loop: {inner_e}")
        except KeyboardInterrupt:
            Log.debug("Server interrupted by user.")

        except Exception as e:
            Log.debug(f"An error occurred: {e}")
        finally:
            event.output_folder_path = None

def test_received_data(data):
    print(f"Received data: {data.decode()}")

if __name__ == '__main__':
    while True:
        listen_for_signal()