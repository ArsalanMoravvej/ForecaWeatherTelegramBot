import os
import signal
import subprocess
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

BOT_SCRIPT = "bot.py"  # Replace with your bot's main script

class RestartHandler(FileSystemEventHandler):
    def __init__(self, process_starter):
        self.process_starter = process_starter

    def on_any_event(self, event):
        if event.is_directory:
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
            self.process.send_signal(signal.SIGTERM)  # Gracefully stop the bot
            self.process.wait()
        self.start_bot()

if __name__ == "__main__":
    process_starter = ProcessStarter()
    event_handler = RestartHandler(process_starter)
    observer = Observer()
    observer.schedule(event_handler, path=".", recursive=True)
    observer.start()

    try:
        while True:
            pass  # Keep running
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
