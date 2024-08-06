import folder_creator
import threading

from log import log_info

def execute_command(signal):
    from main import event
    from config_loader import config
    """根据信号执行对应的操作"""
    if signal == '0001':
        log_info("执行操作1：收到信号 0001")
        # 更新event.usage_count
        event.usage_count += 1
        event.output_folder_path = folder_creator.create_folder(config['output_folder'])
        
        # 更新video_saver_threads字典
        for thread_id in event.video_saver_threads.keys():
            thread = threading._active.get(thread_id)
            if thread is not None and thread.is_alive():
                event.video_saver_threads[thread_id] = 1
            else:
                event.video_saver_threads[thread_id] = 0


        # 更新log_saver_threads字典
        for thread_id in event.log_saver_threads.keys():
            thread = threading._active.get(thread_id)
            if thread is not None and thread.is_alive():
                event.log_saver_threads[thread_id] = 1
            else:
                event.log_saver_threads[thread_id] = 0
        print("执行操作1")
    elif signal == '0002':
        log_info("执行操作2：收到信号 0002")
        # 在这里添加对应的操作代码
        print("执行操作2")
    else:
        log_info(f"收到未知信号: {signal}")
        print("未知信号")

def listen_for_keyboard_input():
    """监听键盘输入"""
    try:
        while True:
            signal = input("请输入信号 (0001, 0002, etc.): ")
            execute_command(signal)
    except KeyboardInterrupt:
        log_info("监听程序被用户中断。")
        print("程序已中断")
if __name__ == '__main__':
    listen_for_keyboard_input()