import threading
from config_loader import config
from log_saver import start_all_docker_logs
from network_listener import listen_for_signal
from video_saver import start_all_cameras
from threading import Lock
from dataclasses import dataclass
from signal_listener import listen_for_keyboard_input
from file_listener import listen_for_file_signal

@dataclass
class Event:
    output_folder_path: str
    log_saver_threads: dict
    video_saver_threads: dict
    usage_count: int
    lock: Lock = Lock()  # 添加锁

# 初始化Event实例
event = Event(
    output_folder_path=None,
    log_saver_threads={},  # 初始化为一个空字典
    video_saver_threads={},  # 初始化为一个空字典
    usage_count=0
)

# 主程序入口
def main():


    # 启动视频缓存进程
    video_thread = threading.Thread(target=start_all_cameras, args=(config,))
    video_thread.start()

    # 启动日志缓存进程
    log_thread = threading.Thread(target=start_all_docker_logs, args=(config,))
    log_thread.start()

    # 启动网络监听线程
    network_listener_thread = threading.Thread(target=listen_for_signal, args=('127.0.0.1', 12345, '0001'))
    network_listener_thread.start()

    # 启动键盘监听线程
    signal_listener_thread = threading.Thread(target=listen_for_keyboard_input)
    signal_listener_thread.start()

    #启动文件监听线程
    listen_for_file_signal_thread = threading.Thread(target=listen_for_file_signal, args=('/home/storage/capture/start.txt',))
    listen_for_file_signal_thread.start()

    # 退出时清理资源
    def cleanup():
        print("清理资源...")
        # 在这里添加进程的清理代码

    try:
        network_listener_thread.join()
        log_thread.join()
        signal_listener_thread.join()
        listen_for_file_signal_thread.join()
        video_thread.join()
    except KeyboardInterrupt:
        cleanup()

if __name__ == "__main__":
    main()
