from log import Log
import threading
import platform

'''
为了多个监控调用一样的服务
将服务写在action.py中
'''
def action1():
    import folder_creator

    from main import event
    from config_loader import config
    Log.debug("进入action1")
    # 更新event.usage_count和output_folder_path
    event.usage_count += 1
    event.output_folder_path = folder_creator.create_folder(
        config['output_folder'])

    # 更新video_saver_threads字典
    for thread_id in event.video_saver_threads.keys():
        thread = threading._active.get(thread_id)
        if thread is not None and thread.is_alive():
            event.video_saver_threads[thread_id] = 1
        else:
            event.video_saver_threads[thread_id] = 0

    #保存日志到文件
    # 检查操作系统
    current_os = platform.system()

    if current_os == "Linux":
        Log.debug("当前系统是 Linux")
        from log_saver import save_docker_logs
        save_docker_logs()

    elif current_os == "Windows":
        Log.debug("当前系统是 Windows")
        from ssh_executer import save_all_docker_logs
        save_all_docker_logs()

    else:
        Log.debug("当前系统不是 Linux 或 Windows")

    Log.debug("结束action1")
if __name__ == '__main__':
    action1()
