import os
import time
from log import Log
from action import action1

def listen_for_file_signal(file_path='D:\\MatrixSoftware\\项目现场同步资料\\补连塔\\test.txt'):
    while True:
        if os.path.exists(file_path):
            with open(file_path, 'r') as f:
                signal = f.read().strip()
                if signal == 'start':  # 检查文件内容是否为'start'
                    action1()  # 如果是，执行action1()
                    Log.info(f"检查到来自{file_path}的内容: {signal}")
                    # 清空文件内容或删除文件
                    open(file_path, 'w').close()  # 清空文件内容
        time.sleep(1)  # 每秒检查一次
if __name__ == '__main__':
    listen_for_file_signal()