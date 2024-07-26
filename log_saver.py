import subprocess
from datetime import datetime

def save_docker_logs(container_name, lines, output_path):
    """保存指定容器的Docker日志"""
    current_time = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
    filename = f"{container_name}_{current_time}.log"
    full_path = os.path.join(output_path, filename)
    with open(full_path, 'w') as file:
        subprocess.run(['docker', 'logs', '--tail', str(lines), container_name], stdout=file)
