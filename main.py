import threading
import os
from config_loader import load_config
from folder_creator import create_folder
from network_listener import listen_for_signal
from video_saver import start_all_cameras, save_video_flag

def main():
    # 加载配置文件
    config_path = '/home/storage/capture/.config/config.yaml'
    config = load_config(config_path)

    # 启动网络监听线程
    listener_thread = threading.Thread(target=listen_for_signal, args=('0.0.0.0', 12345, '0001'))
    listener_thread.start()

    # 启动 Docker 日志缓存进程（此处为示例，请替换为实际功能）
    def docker_log_cache():
        print("Docker 日志缓存进程已启动...")
        # 在这里添加实际的 Docker 日志缓存代码

    docker_thread = threading.Thread(target=docker_log_cache)
    docker_thread.start()

    # 启动视频缓存进程
    video_thread = threading.Thread(target=start_all_cameras)
    video_thread.start()

    # 等待信号以创建文件夹并开始保存数据
    if listen_for_signal('0.0.0.0', 12345, '0001'):
        print("收到信号 0001")
        output_folder = create_folder(config['output_folder'])
        
        # 更新日志和视频保存路径
        log_path = os.path.join(output_folder, "logs")
        video_path = os.path.join(output_folder, "videos")
        
        if not os.path.exists(log_path):
            os.makedirs(log_path)
        if not os.path.exists(video_path):
            os.makedirs(video_path)
        
        # 将路径传递给相应的进程
        # 更新配置文件中的新路径
        config['log_path'] = log_path
        config['video_path'] = video_path
        
        # 通知视频保存模块保存视频到新路径
        save_video_flag.set()

    # 退出时清理资源
    def cleanup():
        print("清理资源...")
        # 在这里添加进程的清理代码

    try:
        listener_thread.join()
        docker_thread.join()
        video_thread.join()
    except KeyboardInterrupt:
        cleanup()

if __name__ == "__main__":
    main()
