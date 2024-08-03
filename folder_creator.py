import os
from datetime import datetime

def create_folder(base_path):
    """创建基于当前日期时间的文件夹"""
    # 获取当前时间
    now = datetime.now()
    # 使用预定义格式化符号，并手动插入中文字符
    current_time = now.strftime("%Y年%m月%d日") + f"{now.hour}时{now.minute}分{now.second}秒"
    # 创建路径
    path = os.path.join(base_path, current_time)
    # 创建文件夹（如果不存在）
    os.makedirs(path, exist_ok=True)
    print(f"文件夹 {path} 创建成功")
    return path

if __name__ == "__main__":
    create_folder("D:\MatrixSoftware\项目现场同步资料\补连塔\.测试记录表\7.28")




