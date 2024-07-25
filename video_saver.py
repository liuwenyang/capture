import cv2
from datetime import datetime

def save_video(rtsp_url, duration, output_path):
    """保存摄像头的视频流"""
    cap = cv2.VideoCapture(rtsp_url)
    current_time = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
    filename = f"{rtsp_url.split('@')[-1]}_{current_time}.mp4"
    full_path = os.path.join(output_path, filename)
    out = cv2.VideoWriter(full_path, cv2.VideoWriter_fourcc(*'mp4v'), 20.0, (640, 480))

    start_time = datetime.now()
    while (datetime.now() - start_time).seconds < duration:
        ret, frame = cap.read()
        if ret:
            out.write(frame)
    cap.release()
    out.release()
# if __name__ == '__main__':
#     #显示视频窗口
#     cv2.namedWindow("Video", cv2.WINDOW_NORMAL)
#     cv2.resizeWindow("Video", 640, 480)
