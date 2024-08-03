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
                        # 回复发送方相同信号+1
                        server_socket.sendto(str(int(signal) + 1).encode(), (_))
                        print(f'回复来自{ip}:{port}的信号: {str(int(signal) + 1)}')
                        # 更新event.usage_count
                        event.usage_count += 1
                        event.output_folder_path = folder_creator.create_folder(config['output_folder'])
                        
                        # 更新log_saver_threads字典
                        for thread_name, thread in event.log_saver_threads.items():
                            if thread.is_alive():
                                event.log_saver_threads[thread_name] = 1
                            else:
                                event.log_saver_threads[thread_name] = 0

                        # 更新video_saver_threads字典
                        for thread_name, thread in event.video_saver_threads.items():
                            if thread.is_alive():
                                event.video_saver_threads[thread_name] = 1
                            else:
                                event.video_saver_threads[thread_name] = 0
                        print(f"流程进入后 event.output_folder_path: {event.output_folder_path}, event.usage_count: {event.usage_count}")
                        print(event.log_saver_threads)
                        print(event.video_saver_threads)
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
