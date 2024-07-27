import cv2
from datetime import datetime
import os
import config_loader  # 引入配置加载模块
from collections import deque
import threading
import socket

config = config_loader.load_config()
save_video_flag = threading.Event()
output_path = config['output_path']
video_length = config['video_length']

def save_video(rtsp_url, video_length):
    """缓存摄像头的视频流"""
    # 打开RTSP流
    cap = cv2.VideoCapture(rtsp_url)

    # 检查是否成功打开流
    if not cap.isOpened():  
        print("无法打开RTSP流")
        return

    # 获取视频的帧宽度和高度
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    # 定义视频编解码器
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')

    print("开始缓存视频帧...")

    # 创建一个双端队列来存储帧
    frame_buffer = deque(maxlen=video_length * 20)  # 假设20 fps

    try:
        while True:
            # 读取一帧
            ret, frame = cap.read()

            # 检查是否成功读取帧
            if not ret:
                print("无法读取帧")
                break

            # 将帧添加到缓存队列
            frame_buffer.append(frame)

            # 检查是否触发保存操作
            if save_video_flag.is_set():
                # 获取当前时间戳
                current_time = datetime.now().strftime("%Y%m%d%H%M%S")
                # 构建输出视频文件的完整路径
                output_file = os.path.join(output_path, f"output_video_{current_time}.mp4")
                
                print(f"保存之前{video_length}秒的视频到 {output_file}...")
                
                # 创建VideoWriter对象
                out = cv2.VideoWriter(output_file, fourcc, 20.0, (frame_width, frame_height))
                
                # 将缓存队列中的帧写入视频文件
                for buffered_frame in frame_buffer:
                    out.write(buffered_frame)

                # 释放VideoWriter对象
                out.release()
                print("视频保存完成")
                save_video_flag.clear()

    finally:
        # 释放VideoCapture对象
        cap.release()
        cv2.destroyAllWindows()



def start_all_cameras():
    threads = []
    for camera in config['camera']:
        t = threading.Thread(target=save_video, args=(camera['rtsp_url'], video_length))
        threads.append(t)
        t.start()

    signal_thread = threading.Thread(target=signal_listener)
    signal_thread.start()

    for t in threads:
        t.join()

if __name__ == '__main__':
    start_all_cameras()
