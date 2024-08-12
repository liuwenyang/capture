from action import action1
from log import Log

def execute_command(signal):
    """根据信号执行对应的操作"""
    if signal == '0001':
        Log.debug("执行操作1：收到信号 0001")
        
        action1()
    elif signal == '0002':
        Log.debug("执行操作2：收到信号 0002")
        # 在这里添加对应的操作代码
        print("执行操作2")
    else:
        Log.debug(f"收到未知信号: {signal}")
        print("未知信号")

def listen_for_keyboard_input():
    """监听键盘输入"""
    try:
        while True:
            signal = input("请输入信号 (0001, 0002, etc.): ")
            execute_command(signal)
    except KeyboardInterrupt:
        Log.debug("监听程序被用户中断。")
        print("程序已中断")
if __name__ == '__main__':
    listen_for_keyboard_input()