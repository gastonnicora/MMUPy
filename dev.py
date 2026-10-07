import subprocess
import sys
import time

from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer

class RestartHandler(FileSystemEventHandler):

    def __init__(self):
        self.process = None
        self.start_process()

    def start_process(self):

        if self.process is not None:
            self.process.terminate()
            self.process.wait()

        self.process = subprocess.Popen(
            [sys.executable, "main.py"]
        )

    def on_modified(self, event):

        if event.is_directory:
            return

        if not event.src_path.endswith(".py"):
            return

        print(f"\nCambio detectado: {event.src_path}")
        print("Reiniciando aplicación...\n")

        self.start_process()


def main():

    handler = RestartHandler()

    observer = Observer()

    observer.schedule(
        handler,
        ".",
        recursive=True
    )

    observer.start()

    try:
        while True:
            time.sleep(1)

    except KeyboardInterrupt:

        observer.stop()

        if handler.process is not None:
            handler.process.terminate()

    observer.join()


if __name__ == "__main__":
    main()