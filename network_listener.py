from fileinput import filename
import socket
from tokenize import Binnumber
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
    from main import event
    from config_loader import config
    with SocketServer(ip, port) as server_socket:
        try:
            while True:
                try:
                    data, _ = server_socket.recvfrom(1024)
                    if data.decode() == signal:
                        print(f'收到来自{ip}:{port}的信号: {data.decode()}')
                        event.usage_count += 1
                        print(f"event.usage_count: {event.usage_count}")
                        print(f"流程进入前event.video_saver: {event.video_saver}, event.log_saver: {event.log_saver}")
                        event.output_folder_path = folder_creator.create_folder(config['output_folder'])
                        print (f"event流程已进入create_folder output_folder_path:{event.output_folder_path}")
                        for docker in config['docker']:
                            print(f"开始保存容器 {config['docker'][docker]['container_name']} 的日志",f" File: {__name__}, Line: {__file__}")
                            event.log_saver += 1
                        for camera in config['camera']:
                            print(f"开始保存摄像头 {config['camera'][camera]['rtsp_url']} 的视频",f" File: {__name__}, Line: {__file__}")
                            event.video_saver += 1
                        if event.video_saver < 1 and event.log_saver < 1:
                            event.output_folder_path = None
                        print(f"流程进入后event.video_saver: {event.video_saver}, event.log_saver: {event.log_saver}")

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
