import os
import time
import win32print
import win32api
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class Watcher:
    def __init__(self, directory_to_watch, extensions):
        self.DIRECTORY_TO_WATCH = directory_to_watch
        self.extensions = extensions
        self.observer = Observer()

    def run(self):
        event_handler = Handler(self.extensions)
        self.observer.schedule(event_handler, self.DIRECTORY_TO_WATCH, recursive=True)
        self.observer.start()
        try:
            while True:
                time.sleep(5)
        except KeyboardInterrupt:
            self.observer.stop()
        self.observer.join()

class Handler(FileSystemEventHandler):
    def __init__(self, extensions):
        self.extensions = extensions

    def on_created(self, event):
        if not event.is_directory and self._is_valid_extension(event.src_path):
            self.print_file(event.src_path)

    def _is_valid_extension(self, file_path):
        # 获取文件扩展名
        ext = os.path.splitext(file_path)[1].lower()
        return ext in self.extensions

    def print_file(self, file_path):
        print(f"Printing: {file_path}")
        # 使用系统的默认打印程序来处理文件
        win32api.ShellExecute(0, "print", file_path, None, ".", 0)


if __name__ == '__main__':
    # 替换为你的微信接收文件的文件夹路径
    path_to_watch = r"C:\Users\Venus\Documents\WeChat Files\wxid_zhtbhn81hnh522\FileStorage\File"
    # 替换为你需要监控的文件扩展名列表
    extensions = ['.pdf', '.doc', '.docx', '.xls', '.xlsx', '.ppt', '.pptx','.jpg','.png']  # 例如监控 PDF 和 TXT 文件
    w = Watcher(path_to_watch, extensions)
    w.run()
