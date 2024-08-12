import inspect
import threading
import logging
import os
'''
DEBUG：调试级别，用于记录开发和调试过程中的信息。这个级别的日志通常是开发者在开发和调试时使用的。
INFO：信息级别，用于记录应用程序的正常运行信息，例如启动、停止、错误等信息。
WARNING：警告级别，用于记录可能会影响应用程序正常运行的警告信息，例如配置错误、网络连接错误等。
ERROR：错误级别，用于记录应用程序运行时出现的错误信息，例如语法错误、运行时错误等。
FATAL：致命级别，用于记录应用程序运行时出现的致命错误信息，例如内存溢出、文件读写错误等。
'''
# 配置日志格式和输出方式
logging.basicConfig(
    level=logging.DEBUG,
    format='\n%(levelname)s - %(asctime)s - %(message)s',
    handlers=[
        logging.StreamHandler()  # 控制台输出
    ]
)

class Log:
    @staticmethod
    def _log(level, message, *args):
        # 获取调用 _log 方法的帧，并向上跳转两次
        current_frame = inspect.currentframe().f_back
        # 往上再跳一帧，获取实际调用 GLog.debug/info/warning/error/fatal 的地方
        caller_frame = current_frame.f_back
        
        # 获取调用者文件名
        current_file = inspect.getfile(caller_frame)
        
        # 获取调用者函数名
        current_function = caller_frame.f_code.co_name
        
        # 获取调用者行号
        current_line = caller_frame.f_lineno
        
        # 获取当前线程ID
        current_thread_id = threading.get_ident()
        
        # 获取当前进程ID
        current_process_id = os.getpid()
        
        # 格式化附加信息
        base_info = f"文件: {current_file}, 行数: {current_line}, 函数: {current_function},  线程ID: {current_thread_id}, 进程ID: {current_process_id}"
        
        # 记录日志信息，根据日志等级决定使用何种方式
        if level == "DEBUG":
            logging.debug(f"{base_info} - {message}", *args)
        elif level == "INFO":
            logging.info(f"{base_info} - {message}", *args)
        elif level == "WARNING":
            logging.warning(f"{base_info} - {message}", *args)
        elif level == "ERROR":
            logging.error(f"{base_info} - {message}", *args)
        elif level == "FATAL":
            logging.critical(f"{base_info} - {message}", *args)
        else:
            logging.warning(f"Unknown logging level: {level}. {base_info} - {message}", *args)

    @staticmethod
    def info(message, *args):
        Log._log("INFO", message, *args)
    
    @staticmethod
    def debug(message, *args):
        Log._log("DEBUG", message, *args)

    @staticmethod
    def warning(message, *args):
        Log._log("WARNING", message, *args)

    @staticmethod
    def error(message, *args):
        Log._log("ERROR", message, *args)
    
    @staticmethod
    def fatal(message, *args):
        Log._log("FATAL", message, *args)

# 示例使用
def example_function():
    Log.debug("这是一个DEBUG等级的日志信息。")
    Log.info("这是一个INFO等级的日志信息。")
    Log.warning("这是一个WARNING等级的日志信息。")
    Log.error("这是一个ERROR等级的日志信息。")
    Log.fatal("这是一个FATAL等级的日志信息。")

if __name__ == "__main__":
    example_function()
