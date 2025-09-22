import hashlib
import pickle
import os
import threading
import time
import logging
from datetime import datetime
from langchain_core.tools import BaseTool
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from logging.handlers import TimedRotatingFileHandler
from collections import deque
from config.root_base import *

log_queue = deque()  # 创建全局日志队列
if not os.path.exists(LOG_DIRECTORY):
    os.makedirs(LOG_DIRECTORY)  # Create directory if it doesn't exist
with open(LOG_QUEUE_FILE, 'wb') as f:
    pickle.dump(log_queue, f)

# Dynamically generate log file name with timestamp
def generate_log_file_name():
    timestamp = datetime.now().strftime("%Y%m%d")
    return os.path.join(LOG_DIRECTORY, f"file_monitor_{timestamp}.log")


# Set up logging configuration with TimedRotatingFileHandler and queue
def setup_logger():
    logger = logging.getLogger("FileMonitorLogger")
    logger.setLevel(logging.INFO)

    log_file_path = generate_log_file_name()

    # 日志处理器 - 写入文件
    handler = TimedRotatingFileHandler(log_file_path, when="midnight", interval=1, backupCount=1)
    formatter = logging.Formatter('%(asctime)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
    handler.setFormatter(formatter)

    # 自定义处理器 - 写入队列
    class QueueHandler(logging.Handler):
        def emit(self, record):
            log_entry = self.format(record)
            if 'created' in log_entry or 'modified' in log_entry:
                with open(LOG_QUEUE_FILE, 'rb') as f:
                    log_queue = pickle.load(f)
                for log in log_queue:
                    if log_entry == log['log_info']:
                        return 0
                log_queue.append({'log_info': log_entry, 'status': 'pending'})  # 将日志放入队列
                save_log_queue_to_file(log_queue)  # 立即保存队列到文件

    queue_handler = QueueHandler()
    queue_handler.setFormatter(formatter)

    # 添加处理器
    logger.addHandler(handler)  # 文件处理器
    logger.addHandler(queue_handler)  # 队列处理器

    return logger

logger = setup_logger()

def calculate_file_hash(file_path):
    """Calculate the SHA-256 hash of a file."""
    sha256_hash = hashlib.sha256()
    with open(file_path, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()


def save_hash_to_store(file_path, hash_value):
    """Save the hash value to the hash store file."""
    with open(HASH_STORE_FILE, 'a') as f:
        f.write(f"{file_path}: {hash_value}\n")
    # logger.info(f"Hash for {file_path} saved: {hash_value}")


def initialize_hash_store():
    """Calculate the hash of all files in the monitored directory and save to hash store."""
    if not os.path.exists(HASH_STORE_FILE):
        open(HASH_STORE_FILE, 'w').close()  # 如果文件不存在则创建空文件

    # logger.info("Initializing hash store with all files in the monitored directory.")
    for root, dirs, files in os.walk(MONITORED_DIRECTORY):
        for file in files:
            file_path = os.path.join(root, file)
            file_hash = calculate_file_hash(file_path)
            save_hash_to_store(file_path, file_hash)

# 存储队列到本地文件
def save_log_queue_to_file(log_queue):
    """将日志队列保存到本地文件中"""
    with open(LOG_QUEUE_FILE, 'wb') as f:
        # print('deque update')
        pickle.dump(log_queue, f)  # 将队列内容序列化存储为文件
    # logger.info(f"Log queue saved to file: {LOG_QUEUE_FILE}")


# 自定义事件处理器类
class FileChangeHandler(FileSystemEventHandler):

    def __init__(self):
        self.last_modified = {}  # 存储文件的上次修改时间
        self.file_hashes = {}  # 存储文件的哈希值

    def on_modified(self, event):
        if not event.is_directory:
            current_time = time.time()
            file_path = event.src_path
            # 如果文件已经存在并且修改时间过短（例如1秒内多次修改），则忽略
            if file_path in self.last_modified and current_time - self.last_modified[file_path] < 2:
                return  # 忽略此事件
            # 记录当前修改时间
            self.last_modified[file_path] = current_time

            # Calculate the new hash of the file
            new_hash = calculate_file_hash(file_path)

            # Compare the new hash with the previous hash
            if file_path in self.file_hashes and self.file_hashes[file_path] == new_hash:
                # logging.info(f'File content not changed: {file_path}')
                return  # Content not changed, ignore this event

            # Update the hash
            self.file_hashes[file_path] = new_hash
            # print('file modified')
            logging.info(rf'File modified: {file_path}')
            # log_queue.appendleft(f'File modified: {file_path}')
            # print(log_queue)
            # self.run_code(file_path)

    def on_created(self, event):
        if not event.is_directory:
            file_path = event.src_path
            file_path = file_path.replace("\\", "/")
            logger.info(rf'File created: {file_path}')
            # log_queue.appendleft(f'File modified: {file_path}')
            # print(log_queue)
            initial_hash = calculate_file_hash(file_path)
            self.file_hashes[file_path] = initial_hash
            save_hash_to_store(file_path, initial_hash)
            # print('file modified')
            # logger.info(f"File created and hash stored for {file_path}")

# 定义监控启动工具类
class MonitorStartTool(BaseTool):
    name: str = "observation_program_start_tool"
    description: str = ("Tool to start a program to observe the file changes in the environment folder, logging the "
                        "events as they happen")

    def _run(self):
        return self.start_monitoring(MONITORED_DIRECTORY)

    def _arun(self):
        raise NotImplementedError("monitor_start_tool does not support async")

    def start_monitoring(self, directory_path: str):
        if not os.path.exists(directory_path):
            raise ValueError(f"Directory {directory_path} does not exist")
        with open(SYSTEM_FILE_PATH, 'rb') as f:
            system_file = pickle.load(f)
        if system_file['environment_observation_program'] == 'START':
            return (f"Observation program has activated for {directory_path} in the background, you need to check the "
                    f"updates in the environment folder.")

        print('#####\nSTART ENVIRONMENT OBSERVATION PROGRAM!\n#####')
        # 初始化时计算所有文件的hash并存储
        initialize_hash_store()

        event_handler = FileChangeHandler()
        observer = Observer()

        # 递归设置为 True 以监控所有子文件夹及其内容
        observer.schedule(event_handler, directory_path, recursive=True)

        logger.info(f"Started observing the folder: {directory_path}")
        observer.start()

        def run_observer():
            try:
                while True:
                    time.sleep(1)
            except KeyboardInterrupt:
                observer.stop()
            observer.join()

        # Start the observer in a separate thread
        monitoring_thread = threading.Thread(target=run_observer)
        monitoring_thread.daemon = True  # This makes sure the thread will exit when the main program does
        monitoring_thread.start()
        system_file['environment_observation_program'] = 'START'
        with open(SYSTEM_FILE_PATH, 'wb') as f:
            pickle.dump(system_file, f)
        # Return immediately, while the monitoring happens in the background
        return f"Observation program is activated for {directory_path} in the background."

    def stop_monitoring(self):
        """Stop the monitoring process."""
        print('stop')
        if self.observer:
            logger.info("Stopping the monitoring process...")
            self.observer.stop()
            self.observer.join()  # 确保监控线程完全停止
            logger.info("Monitoring stopped.")
            return "Monitoring has been stopped."
        else:
            return "No monitoring is currently running."

class MonitorStopTool(BaseTool):
    name: str = "monitor_stop_tool"
    description: str = "Tool to stop monitoring a directory for file changes"

    def __init__(self, monitor_tool: MonitorStartTool):
        self.monitor_tool = monitor_tool  # 接受一个 MonitorStartTool 实例

    def _run(self):
        return self.monitor_tool.stop_monitoring()

    def _arun(self):
        raise NotImplementedError("monitor_stop_tool does not support async")


if __name__ == "__main__":
    start_tool = MonitorStartTool()
    start_tool._run()
    try:
        while True:
            time.sleep(1)
    finally:
        print('end')
    # save_log_queue_to_file()  # 在程序退出前保存队列


