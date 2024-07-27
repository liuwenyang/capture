import threading
import cv2
from datetime import datetime
import os
import config_loader  # 引入配置加载模块
from collections import deque
import network_listener from start_save_flag  # type: ignore # 引入网络监听模块，并获取start_save_flag

config = config_loader.load_config()

output_path = config['output_path']
video_length = config['video_length']

def save_video(rtsp_url,video_name, video_length, output_path):
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
            if start_save_flag.is_set(): # type: ignore
                # 获取当前时间并格式化为字符串
                now = datetime.now()
                current_time = now.strftime("%Y年%m月%d日") + f"{now.hour}时{now.minute}分{now.second}秒"
                # 构建输出视频文件的完整路径
                output_file = os.path.join(output_path, f"{current_time}.mp4")
                
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
        t = threading.Thread(target=save_video, args=(camera['rtsp_url'],camera['name'], camera['video_length'], output_path))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

if __name__ == '__main__':
    start_all_cameras()
