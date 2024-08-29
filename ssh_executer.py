import datetime  
import paramiko
import os
# from config_loader import load_config
from log import Log
from config_loader import config

'''
Paramiko日志太多
减少这些调试日志的输出，在Paramiko库的日志配置中调整日志级别
'''
import logging

# 将Paramiko的日志级别设置为WARNING
logging.getLogger("paramiko").setLevel(logging.WARNING)

# 如果还想要完全关闭日志，可以使用更高的级别，比如ERROR或CRITICAL
logging.getLogger("paramiko").setLevel(logging.ERROR)


def create_ssh_instance(hostname, username, password):
    # 服务器信息
    # hostname = "10.226.13.24" # 替换为你的服务器IP地址 这里是补连塔751
    # username = "root"  # 替换为你的用户名
    # password = "matrixai@2"  # 替换为你的密码
    """创建SSH实例并返回连接"""
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname=hostname, username=username, password=password)
    return ssh


def save_docker_logs(container_name, hosts_name,log_lines, ssh_client):
    """将远程Docker容器的日志保存到本地指定路径"""
    from main import event
    # 远程服务器上的临时文件路径
    # 获取当前时间并格式化为字符串
    now = datetime.datetime.now()
    current_time = now.strftime("%Y年%m月%d日") + f"{now.hour}时{now.minute}分{now.second}秒"
    remote_temp_log_file = f"/tmp/{hosts_name}_{container_name}_{current_time}.logs.txt"

    # 生成 Docker 日志命令，并将日志输出保存到远程的临时文件中
    cmd = f"docker logs --tail {log_lines} {
        container_name} > {remote_temp_log_file}"
    stdin, stdout, stderr = ssh_client.exec_command(cmd)
    stdout.channel.recv_exit_status()  # 等待命令执行完成,否则执行时间过长,下载的是空文件!

    # 使用SFTP将远程的日志文件下载到本地
    sftp_client = ssh_client.open_sftp()
    local_log_file = os.path.join(event.output_folder_path, f"{hosts_name}_{container_name}_{current_time}.logs.txt")
    sftp_client.get(remote_temp_log_file, local_log_file)

    # 删除远程的临时文件
    sftp_client.remove(remote_temp_log_file)
    
    # 关闭SFTP连接
    sftp_client.close()

    Log.info(f"容器{container_name}的{log_lines}行日志文件已保存到本地: {local_log_file}")


def save_all_docker_logs():
    from config_loader import config
    for key in config['docker']:
        docker = config['docker'][key]
        ssh = create_ssh_instance(docker['hosts'], 'root', docker['password'])
        save_docker_logs(docker['container_name'], docker['hosts_name'], docker['log_lines'], ssh)
        ssh.close()
if __name__ == '__main__':
    save_all_docker_logs()



    # ssh = create_ssh_instance_1()
    # save_docker_logs("cli", 100, "D:\\MatrixSoftware\\项目现场同步资料\\补连塔", ssh)

