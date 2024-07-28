import threading
import os
from config_loader import load_config
from folder_creator import create_folder
from network_listener import listen_for_signal
from video_saver import start_all_cameras, save_video_flag
from log_saver import save_docker_logs

# 主程序入口
def main():
    # 加载配置文件
    config_path = '/home/storage/capture/.config/config.yaml'
    #使用单例模式 确保config是全局唯一的
    config = load_config(config_path)

    # 启动网络监听线程
    listener_thread = threading.Thread(target=listen_for_signal, args=('127.0.0.1', 12345, '0001'))
    listener_thread.start()

    # 启动视频缓存进程
    video_thread = threading.Thread(target=start_all_cameras)
    video_thread.start()

    # 退出时清理资源
    def cleanup():
        print("清理资源...")
        # 在这里添加进程的清理代码

    try:
        listener_thread.join()
        video_thread.join()
    except KeyboardInterrupt:
        cleanup()

if __name__ == "__main__":
    main()
