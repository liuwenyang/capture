import subprocess
import threading
from datetime import datetime
import os


def save_docker_logs(container_name, lines):
    from main import event
    """保存指定容器的Docker日志"""
    # 检查容器名是否存在
    result = subprocess.run(['docker', 'ps', '-q', '--filter', f'name={container_name}'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    
    if result.returncode != 0 or not result.stdout.strip():
        print(f"容器 {container_name} 不存在")
        event.log_saver -= 1
        return
    print(f"流程进入save_docker_logs前event.video_saver: {event.video_saver}, event.log_saver: {event.log_saver}, event.output_folder_path: {event.output_folder_path}, event.usage_count: {event.usage_count}")

    while True:
        if event.output_folder_path is not None and event.log_saver > 0:

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
                event.log_saver -= 1
            print(f"容器 {container_name} 的日志已保存到 {full_path}")


def start_all_docker_logs(config):
    """启动所有Docker容器并保存它们的日志"""
    from main import event
    event.log_saver_threads = []
    from main import event
    # 遍历容器ID并保存日志
    for docker in config['docker']:
        print(f"开始保存容器 {config['docker'][docker]['container_name']} 的日志")
        t = threading.Thread(target=save_docker_logs, args=(config['docker'][docker]['container_name'], config['docker'][docker]['log_lines']))
        event.log_saver_threads.append(t)
        t.start()

    for t in event.log_saver_threads:
        t.join()


if __name__ == "__main__":
    container_name = "your_container_name"  # 替换为实际的容器名称
    lines = 100  # 替换为要保存的日志行数
    output_path = "/path/to/output_folder"  # 替换为实际的输出文件夹路径
    save_docker_logs(container_name, lines, output_path)
