import socket
import threading

start_save_flag = threading.Event()

def listen_for_signal(ip='127.0.0.1', port=12345, signal='0001'):
    """监听特定信号来更改全局标志位"""
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind((ip, port))
    print(f"Listening for signal '{signal}' on {ip}:{port}")

    try:
        while True:
            data, _ = server_socket.recvfrom(1024)
            if data.decode() == signal:
                start_save_flag.set()
                print(f'收到信号:{data.decode()}')
                start_save_flag.set()
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        server_socket.close()
        print("Server socket closed.")

if __name__ == '__main__':
    try:
        listen_for_signal()
    except KeyboardInterrupt:
        print("Server interrupted by user.")
    finally:
        start_save_flag.clear()
