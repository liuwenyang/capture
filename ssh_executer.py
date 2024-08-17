import paramiko
import os
#from config_loader import load_config
from log import Log

def create_ssh_instance_1():
    # 服务器信息
    hostname = "10.226.13.24" # 替换为你的服务器IP地址 这里是补连塔751
    username = "root"  # 替换为你的用户名
    password = "matrixai@2"  # 替换为你的密码

    """创建SSH实例并返回连接"""
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname=hostname, username=username, password=password)
    return ssh

def save_docker_logs(container_name, log_lines, save_path, ssh_client):
    """将远程Docker容器的日志保存到本地指定路径"""
    
    # 远程服务器上的临时文件路径
    remote_temp_log_file = f"/tmp/{container_name}_logs.txt"
    
    # 生成 Docker 日志命令，并将日志输出保存到远程的临时文件中
    cmd = f"docker logs --tail {log_lines} {container_name} > {remote_temp_log_file}"
    ssh_client.exec_command(cmd)
    
    # 使用SFTP将远程的日志文件下载到本地
    sftp_client = ssh_client.open_sftp()
    local_log_file = os.path.join(save_path, f"{container_name}_logs.txt")
    sftp_client.get(remote_temp_log_file, local_log_file)
    
    # 关闭SFTP连接
    sftp_client.close()
    
    
    Log.info(f"日志文件已保存到本地: {local_log_file}")

if __name__ == '__main__':
    ssh = create_ssh_instance_1()
    save_docker_logs("cli", 100, "D:\MatrixSoftware\项目现场同步资料\补连塔", ssh)

