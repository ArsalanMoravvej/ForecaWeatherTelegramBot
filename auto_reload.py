import os
import signal
import subprocess
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

BOT_SCRIPT = "main.py"  # Your main bot script
WATCH_DIR = "."  # Watch the entire project folder
IGNORE_DIRS = {".git", "__pycache__"}  # Directories to ignore
IGNORE_EXTENSIONS = {".swp", ".tmp", ".pyc"}  # File extensions to ignore

class RestartHandler(FileSystemEventHandler):
    def __init__(self, process_starter):
        self.process_starter = process_starter

    def on_any_event(self, event):
        # Ignore directories and specified file types
        if event.is_directory or any(ignored in event.src_path for ignored in IGNORE_DIRS) \
                or event.src_path.endswith(tuple(IGNORE_EXTENSIONS)):
            return

        print(f"File changed: {event.src_path}. Restarting bot...")
        self.process_starter.restart_bot()

class ProcessStarter:
    def __init__(self):
        self.process = None
        self.start_bot()

    def start_bot(self):
        self.process = subprocess.Popen(["python", BOT_SCRIPT])

    def restart_bot(self):
        if self.process:
            self.process.send_signal(signal.SIGTERM)  # Gracefully stop
            self.process.wait()
        self.start_bot()

if __name__ == "__main__":
    process_starter = ProcessStarter()
    event_handler = RestartHandler(process_starter)
    observer = Observer()
    observer.schedule(event_handler, path=WATCH_DIR, recursive=True)  # Recursively watch all subdirectories
    observer.start()

    try:
        while True:
            pass  # Keep running
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
