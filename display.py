import cv2  # 导入OpenCV库

def display_frame(frame):
    """Display the given frame."""
    cv2.namedWindow('Camera Stream', cv2.WINDOW_NORMAL)  # 创建可调整大小的窗口
    cv2.imshow('Camera Stream', frame)  # 创建一个窗口并显示图像
    if cv2.waitKey(1) & 0xFF == ord('q') or cv2.getWindowProperty('Camera Stream', cv2.WND_PROP_VISIBLE) < 1:
        raise SystemExit("User exited or window closed.")  # 窗口关闭或用户按'q'退出