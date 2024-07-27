import subprocess
from datetime import datetime
import os

def save_docker_logs(container_name, lines, output_path):
    """保存指定容器的Docker日志"""
    # 获取当前时间并格式化为字符串
    now = datetime.now()
    current_time = now.strftime("%Y年%m月%d日") + f"{now.hour}时{now.minute}分{now.second}秒"
    # 构建日志文件名
    filename = f"{container_name}_{current_time}.log"
    # 构建完整的文件路径
    full_path = os.path.join(output_path, filename)
    # 创建日志文件并将docker日志写入其中
    with open(full_path, 'w') as file:
        subprocess.run(['docker', 'logs', '-t', '--tail', str(lines), container_name], stdout=file)
    print(f"日志已保存到 {full_path}")

if __name__ == "__main__":
    container_name = "your_container_name"  # 替换为实际的容器名称
    lines = 100  # 替换为要保存的日志行数
    output_path = "/path/to/output_folder"  # 替换为实际的输出文件夹路径
    save_docker_logs(container_name, lines, output_path)
