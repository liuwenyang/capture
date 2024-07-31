import threading
import cv2
from datetime import datetime
import os
from collections import deque
import inspect

    
def save_video(rtsp_url, video_length=30, video_name='default'):
    from main import event
    # 获取当前栈帧信息
    frame = inspect.currentframe()
    # 获取调用者的栈帧信息
    caller_frame = frame.f_back
    # 获取函数名
    function_name = caller_frame.f_code.co_name
    # 获取文件名
    file_name = caller_frame.f_code.co_filename
    # 获取行号
    line_number = caller_frame.f_lineno
    """缓存摄像头的视频流"""
    event.video_saver += 1
    # 打开RTSP流
    cap = cv2.VideoCapture(rtsp_url)

    # 检查是否成功打开流
    if not cap.isOpened():  
        print(f"无法打开{rtsp_url}的RTSP流")
        event.video_saver -= 1
        return

    # 获取视频的帧宽度和高度
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    # 定义视频编解码器
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')

    print(f"开始缓存{rtsp_url}{video_name}的视频帧...")

    # 创建一个双端队列来存储帧
    frame_buffer = deque(maxlen=video_length * 20)  # 假设20 fps

    print(f"流程进入save_video前event.video_saver: {event.video_saver}, event.log_saver: {event.log_saver}, event.output_folder_path: {event.output_folder_path}, event.usage_count: {event.usage_count}")

    try:
        while True:
            # 读取一帧
            ret, frame = cap.read()

            # 检查是否成功读取帧
            if not ret:
                print("无法读取帧")
                event.video_saver -= 1
                break

            # 将帧添加到缓存队列
            frame_buffer.append(frame)

            # 如果路径非空           
            if event.output_folder_path is not None and event.video_saver > 0:

                # 获取当前时间并格式化为字符串
                now = datetime.now()
                current_time = now.strftime("%Y年%m月%d日") + f"{now.hour}时{now.minute}分{now.second}秒"
                # 构建输出视频文件的完整路径
                output_file = os.path.join(event.output_folder_path, f"{video_name}_{current_time}.mp4")
                
                print(f"保存之前{video_length}秒的视频到 {output_file}开始")
                
                # 创建VideoWriter对象
                out = cv2.VideoWriter(output_file, fourcc, 20.0, (frame_width, frame_height))
                
                # 将缓存队列中的帧写入视频文件
                for buffered_frame in frame_buffer:
                    out.write(buffered_frame)

                # 释放VideoWriter对象
                out.release()
                print("视频保存完成")
                event.video_saver -= 1
                print(f"event.video_saver: {event.video_saver}",f" File: {__name__}, Line: {line_number},Function: {function_name},")
                print(f"流程进入save_video后event.video_saver: {event.video_saver}, event.log_saver: {event.log_saver}, event.output_folder_path: {event.output_folder_path}, event.usage_count: {event.usage_count}")

    finally:
        # 释放VideoCapture对象
        cap.release()
        cv2.destroyAllWindows()
        event.video_saver -= 1
        print(f"event.video_saver: {event.video_saver}",f" File: {__name__}, Line: {line_number},Function: {function_name},")




def start_all_cameras(config):
    from main import event
    threads = []
    for camera in config['camera']:
        print(f"开始缓存{config['camera'][camera]['name']}的视频流...")
        t = threading.Thread(target=save_video, args=(config['camera'][camera]['rtsp_url'], config['camera'][camera]['video_length'], config['camera'][camera]['name']))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

if __name__ == '__main__':
    start_all_cameras()