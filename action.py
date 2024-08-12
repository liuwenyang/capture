from log import Log
import threading

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

    # 更新log_saver_threads字典
    for thread_id in event.log_saver_threads.keys():
        thread = threading._active.get(thread_id)
        if thread is not None and thread.is_alive():
            event.log_saver_threads[thread_id] = 1
        else:
            event.log_saver_threads[thread_id] = 0

    Log.debug("结束action1")
if __name__ == '__main__':
    action1()
