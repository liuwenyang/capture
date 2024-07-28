import socket
import threading
import queue
import folder_creator
from config_loader import load_config
from log_saver import start_all_docker_logs
# 创建一个 Queue 对象 保存路径信息
q = queue.Queue()
# 加载配置文件
config_path = '/home/storage/capture/.config/config.yaml'
#使用单例模式 确保config是全局唯一的
config = load_config(config_path)

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
                    path = folder_creator.create_folder(config['output_folder'])
                    q.put(path)
                    print(f"path: {path}已存入队列")
                    #start_all_docker_logs(config,path)
                    
                    
        except KeyboardInterrupt:
            print("Server interrupted by user.")
        except Exception as e:
            print(f"An error occurred: {e}")
        finally:
            q.clear()

if __name__ == '__main__':
    try:
        listen_for_signal()
    except Exception as e:
        print(f"Unexpected error: {e}")
