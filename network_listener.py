import socket

def listen_for_signal(ip='0.0.0.0', port=12345, signal='0001'):
    """监听特定信号来更改全局标志位"""
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind((ip, port))
    while True:
        data, _ = server_socket.recvfrom(1024)
        if data.decode() == signal:
            return True
    return False
