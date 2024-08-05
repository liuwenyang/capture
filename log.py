import inspect
import threading
import logging
import os

# 配置日志格式和输出方式
logging.basicConfig(
    level=logging.DEBUG,
    format='\n%(levelname)s - %(asctime)s - %(message)s',
    handlers=[
        logging.StreamHandler()  # 控制台输出
    ]
)

def log_info(message, *args):
    # 获取当前帧信息
    current_frame = inspect.currentframe().f_back  # f_back跳转到上一层调用者帧
    
    # 获取当前文件名
    current_file = inspect.getfile(current_frame)
    
    # 获取当前函数名
    current_function = current_frame.f_code.co_name
    
    # 获取当前行号
    current_line = current_frame.f_lineno
    
    # 获取当前线程ID
    current_thread_id = threading.get_ident()
    
    # 获取当前进程ID
    current_process_id = os.getpid()
    
    # 格式化附加信息
    base_info = f"文件: {current_file}, 行数: {current_line}, 函数: {current_function},  线程ID: {current_thread_id}, 进程ID: {current_process_id}"
    
    # 记录日志信息
    logging.debug(f"{base_info} - {message}", *args)

def example_function():
    log_info("这是一个示例函数中的日志信息。")
    print("这是一个示例函数。")

if __name__ == "__main__":
    example_function()
    
    # 示例多线程环境下的使用
    def threaded_function():
        log_info("线程函数中的日志信息。")
        print("线程函数正在运行。")
    
    thread = threading.Thread(target=threaded_function)
    thread.start()
    thread.join()
