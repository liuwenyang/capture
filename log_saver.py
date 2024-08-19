import subprocess
import threading
import os
from log import Log


def save_docker_logs(container_name, lines):
    """保存指定容器的Docker日志"""
    from main import event
    from datetime import datetime

    # 获取当前时间并格式化为字符串
    now = datetime.now()
    current_time = now.strftime("%Y年%m月%d日") + f"{now.hour}时{now.minute}分{now.second}秒"
    # 构建日志文件名
    filename = f"{container_name}_{current_time}.log"
    # 构建完整的文件路径
    full_path = os.path.join(event.output_folder_path, filename)
    # 创建日志文件并将docker日志写入其中
    with open(full_path, 'w') as file:
        subprocess.run(['docker', 'logs', '--tail', str(lines), container_name], stdout=file)
        event.log_saver_threads [threading.get_ident()] = None
    Log.debug(f"容器 {container_name} 的日志已保存到 {full_path}")


def start_all_docker_logs():
    """启动所有Docker容器并保存它们的日志"""
    from config_loader import config
    # 遍历容器ID并保存日志
    for docker in config['docker']:
        Log.debug(f"开始保存容器 {config['docker'][docker]['container_name']} 的日志")
        save_docker_logs(config['docker'][docker]['container_name'], config['docker'][docker]['log_lines'])


if __name__ == "__main__":
    start_all_docker_logs()
