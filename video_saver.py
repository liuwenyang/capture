import cv2
from datetime import datetime
import os
import config_loader  # 引入配置加载模块
from collections import deque

config = config_loader.load_config()

def save_video(rtsp_url, video_length):
    """缓存摄像头的视频流"""
    # 打开RTSP流
    cap = cv2.VideoCapture(rtsp_url)

    # 检查是否成功打开流
    if not cap.isOpened():  
        print("无法打开RTSP流")
        exit()

    # 获取视频的帧宽度和高度
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    # 定义视频编解码器
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')

    print("开始缓存视频帧...")

    # 创建一个列表来存储帧
    frame_buffer = []

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
                output_file = f"{output_path}output_video_{current_time}.mp4"
                
                print(f"保存之前30秒的视频到 {output_file}...")
                
                # 创建VideoWriter对象
                out = cv2.VideoWriter(output_file, fourcc, 20.0, (frame_width, frame_height))
                
                # 将缓存队列中的帧写入视频文件
                for buffered_frame in frame_buffer:
                    out.write(buffered_frame)

                # 释放VideoWriter对象
                out.release()
                print("视频保存完成")
                break

    finally:
        # 释放VideoCapture对象
        cap.release()
        cv2.destroyAllWindows()


#if __name__ == '__main__':
