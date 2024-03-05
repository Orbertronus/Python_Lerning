import time
import requests
import os
from threading import Thread


# CPU-bound task (heavy computation)
def encrypt_file(path: str):
    print(f"Processing file from {path} in process {os.getpid()}")
    # Just simulate a heavy computation
    _ = [i for i in range(100_000_000)]


# I/O-bound task (downloading image from URL)
def download_image(image_url):
    print(f"Downloading image from {image_url} in thread {Thread.current_thread().name}")
    response = requests.get(image_url)
    with open("image.jpg", "wb") as f:
        f.write(response.content)

def using_threads():
    threads: list[Thread] = [
        Thread(target=encrypt_file, args=("rockyou.txt")),
        Thread(target=download_image, args=("https://picsum.photos/1000/1000")),
    ]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()

if __name__ == "__main__":
    start = time.perf_counter()
    try:
        using_threads()
    
    # print(f"Time taken for encryption task: {encryption_counter}, I/O-bound task: {download_counter}, Total: {total} seconds")
        print(f"Total: {time.perf_counter() - start}")
    except Exception as e:
        print(f"Error occurred: {e}")
