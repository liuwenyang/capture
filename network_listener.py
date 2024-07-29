import socket
import folder_creator
from config_loader import config
from log_saver import start_all_docker_logs


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

    with SocketServer(ip, port) as server_socket:
        try:
            while True:
                try:
                    data, _ = server_socket.recvfrom(1024)
                    if data.decode() == signal:
                        print(f'收到来自{ip}:{port}的信号: {data.decode()}')
                        if event.video_saver < 1 and event.log_saver < 1:

                            output_folder_path = folder_creator.create_folder(config['output_folder'])
                            event.output_folder_path = output_folder_path
                            print (f"event流程已进入output_folder_path: {event.output_folder_path}")
                            start_all_docker_logs(config, output_folder_path)
                except Exception as inner_e:
                    print(f"An error occurred inside loop: {inner_e}")
        except KeyboardInterrupt:
            print("Server interrupted by user.")
        except Exception as e:
            print(f"An error occurred: {e}")
        finally:
            output_folder_path = None


if __name__ == '__main__':
    try:
        listen_for_signal()
    except Exception as e:
        print(f"Unexpected error: {e}")
