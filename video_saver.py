import threading
import cv2
from datetime import datetime
import os
from collections import deque
from log import log_info
'''
OpenCV窗口处理错误：
cv2.error: OpenCV(...) error: The function is not implemented. Rebuild the library with Windows, GTK+ 2.x or Cocoa support. 
这说明OpenCV未配置用于显示窗口。这个问题在无图形界面的Docker环境中常见，因为缺少GUI支持库。
在无图形界面的环境中运行时（例如Docker中），如果不需要显示窗口，可以跳过 cv2.destroyAllWindows() 或者在构建时安装必要的GUI支持库。
'''
# Check if running in a headless environment
if hasattr(cv2, 'getBuildInformation'):
    build_info = cv2.getBuildInformation()
    if 'Video I/O:' in build_info and 'GUI:' not in build_info:
        def destroy_windows():
            pass
    else:
        def destroy_windows():
            cv2.destroyAllWindows()
else:
    def destroy_windows():
        cv2.destroyAllWindows()


def save_video(rtsp_url, video_length=30, video_name='default'):
    from main import event


    """缓存摄像头的视频流"""
    # 打开RTSP流
    cap = cv2.VideoCapture(rtsp_url)

    # 检查是否成功打开流
    if not cap.isOpened():  
        print(f"无法打开{rtsp_url}的RTSP流")
        event.video_saver_threads[threading.get_ident()] = None
        return
    else:
        print(f"开始缓存{rtsp_url}{video_name}的视频帧...")

    # 获取视频的帧宽度和高度
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    # 定义视频编解码器
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')


    # 创建一个双端队列来存储帧
    frame_buffer = deque(maxlen=video_length * 20)  # 假设20 fps


    try:
        while True:
            # 读取一帧
            ret, frame = cap.read()

            # 检查是否成功读取帧
            if not ret:
                print("无法读取帧")
                event.video_saver_threads[threading.get_ident()] = None
                break

            # 将帧添加到缓存队列
            frame_buffer.append(frame)

            # 如果路径非空           
            if event.output_folder_path is not None and event.video_saver_threads[threading.get_ident()] is not None:

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
                event.video_saver_threads[threading.get_ident()] = None



    finally:
        # 释放VideoCapture对象
        cap.release()
        destroy_windows()

        event.video_saver_threads[threading.get_ident()] = None





def start_all_cameras(config):
    from main import event
    for camera in config['camera']:
        #print(f"开始缓存{config['camera'][camera]['name']}的视频流...")
        t = threading.Thread(target=save_video, args=(config['camera'][camera]['rtsp_url'], config['camera'][camera]['video_length'], config['camera'][camera]['name']))
        # 使用线程ID作为字典的键，值设为空（或者根据需要设置其他初始值）

        t.start()
        event.video_saver_threads[t.ident] = None #在存储线程对象之前，确保线程已经启动，这样才能确保 t.ident 返回正确的线程ID：
        log_info(f"event.video_saver_threads: {event.video_saver_threads}")
    # 使用线程对象来调用 join() 方法
    for t in threading.enumerate():
        if t.ident in event.video_saver_threads:
            t.join()

if __name__ == '__main__':
    start_all_cameras()