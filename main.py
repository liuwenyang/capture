import threading
import os
from config_loader import SingletonConfig
from network_listener import listen_for_signal config
from video_saver import start_all_cameras


# 主程序入口
def main():
    # 加载配置文件
    config_singleton = SingletonConfig("D:\开源项目\capture\config.yaml")
    config = config_singleton.get_config()
    # 启动网络监听线程
    listener_thread = threading.Thread(target=listen_for_signal, args=('127.0.0.1', 12345, '0001'))
    listener_thread.start()

    # 启动视频缓存进程
    video_thread = threading.Thread(target=start_all_cameras,args=config)
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
