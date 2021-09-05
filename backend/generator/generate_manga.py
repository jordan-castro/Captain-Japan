from backend.data.dir import manga_dir

from pathlib import Path
from threading import Thread
import os


def generate_manga(data, directory):
    """
    Generate a manga.

    Params:
        - <data: list(int, list(bytes))> data used when generating.
        - <directory: str> the directory name of the manga. Usually just a title.

    Return: <list(str)> image paths.
    """
    base_path = f"{manga_dir()}{directory}"
    chapter_path = f"{base_path}/Chapter_{data[0]}"

    # Check if directory does not exists
    if not Path(base_path).exists():
        # Make it
        os.mkdir(base_path)
    # Check if chapter directory does not exist
    if not Path(chapter_path).exists():
        # Make it
        os.mkdir(chapter_path)

    threads = []
    image_paths = []

    # Loop through image data passed
    for image in data[1]:
        # Generate image path
        image_path = f"{chapter_path}/image_{data[1].index(image)}.png"
        image_paths.append(image_path)

        # Write images in threads
        t = Thread(target=generate_image, args=(image.content, image_path))
        threads.append(t)
        t.start()
    
    # Close threads
    for thread in threads:
        thread.join()

    return image_paths


def generate_image(image_data, path):
    """
    Generate a image.

    Params:
        - <image_data: bytes> the bytes of the image.
        - <path: str> where the image will be.
    """
    if not image_data:
        return 

    with open(path, "wb") as image:
        image.write(image_data) 