import logging
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler, FileSystemEvent


class Watcher:
    def __init__(self, directories):
        self.directories = directories
        self.observer = Observer()

    def run(self):
        # Set up a handler and observer for each directory
        event_handler = Handler()
        for directory in self.directories:
            self.observer.schedule(event_handler, directory, recursive=True)
        self.observer.start()
        logging.info("Observer started")
        try:
            while True:
                time.sleep(10)
        except KeyboardInterrupt:
            self.observer.stop()
            logging.info("Observer stopped")
        self.observer.join()

class Handler(FileSystemEventHandler):
    def on_created(self, event):
        if not event.is_directory:
            logging.info(f"File created: {event.src_path}")

    def on_modified(self, event):
        if not event.is_directory:
            print(f"File modified: {event.src_path}")
            # Add processing logic here for modified files

    def on_deleted(self, event):
        if not event.is_directory:
            print(f"File deleted: {event.src_path}")
            # Add processing logic here for deleted files

