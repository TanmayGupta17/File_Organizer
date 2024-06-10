from os import scandir, rename, mkdir
import os
from os.path import splitext, exists, join
from shutil import move
from time import sleep
import logging
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# Supported file extensions
image_extensions = [
    ".jpg", ".jpeg", ".jpe", ".jif", ".jfif", ".jfi", ".png", ".gif", ".webp", ".tiff", ".tif", ".psd", ".raw",
    ".arw", ".cr2", ".nrw", ".k25", ".bmp", ".dib", ".heif", ".heic", ".ind", ".indd", ".indt", ".jp2", ".j2k",
    ".jpf", ".jpx", ".jpm", ".mj2", ".svg", ".svgz", ".ai", ".eps", ".ico"
]

video_extensions = [
    ".webm", ".mpg", ".mp2", ".mpeg", ".mpe", ".mpv", ".ogg", ".mp4", ".mp4v", ".m4v", ".avi", ".wmv", ".mov", 
    ".qt", ".flv", ".swf", ".avchd"
]

# Directories
source_dir = "/Users/tanmaygupta/Downloads"
dest_dir_images = "/Users/tanmaygupta/Desktop/Downloaded Images"
dest_dir_videos = "/Users/tanmaygupta/Desktop/Downloaded Videos"

# Ensure destination directories exist
if not exists(dest_dir_images):
    mkdir(dest_dir_images)

if not exists(dest_dir_videos):
    mkdir(dest_dir_videos)

def make_unique(dest, name):
    filename, extension = splitext(name)
    counter = 1
    while exists(join(dest, name)):
        name = f"{filename}({counter}){extension}"
        counter += 1
    return name

def move_file(dest, entry, name):
    if exists(join(dest, name)):
        unique_name = make_unique(dest, name)
        old_name = join(dest, name)
        new_name = join(dest, unique_name)
        rename(old_name, new_name)
    move(entry, dest)

class MoveHandler(FileSystemEventHandler):
    def on_modified(self, event):
        with scandir(source_dir) as entries:
            for entry in entries:
                if entry.is_file():
                    name = entry.name
                    self.check_and_move(entry, name)

    def check_and_move(self, entry, name):
        if any(name.lower().endswith(ext) for ext in video_extensions):
            move_file(dest_dir_videos, entry.path, name)
            logging.info(f"Moved video file: {name}")
        elif any(name.lower().endswith(ext) for ext in image_extensions):
            move_file(dest_dir_images, entry.path, name)
            logging.info(f"Moved image file: {name}")

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
    monitored_path = source_dir  # Renamed to avoid conflict
    event_handler = MoveHandler()
    observer = Observer()
    observer.schedule(event_handler, monitored_path, recursive=True)
    observer.start()
    try:
        while True:
            sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
