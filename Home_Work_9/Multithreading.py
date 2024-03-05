import time
import requests
from pathlib import Path
from threading import Thread, current_thread
global encryption_counter
global download_counter
encryption_counter = 0
download_counter = 0

class File:
    def __init__(self, file_path: str, mode: str):
        self.file_path = file_path
        self.mode = mode
        try:
            self.file = open(self.file_path, self.mode)
        except IOError as e:
            raise IOError(f"Произошла ошибка: {e}")

    def close(self):
        self.file.close()

# Задача, требующая много ресурсов ЦП (значительные вычисления)
def encrypt_file(file_1: File):
    global encryption_counter
    start_timer = time.perf_counter()
    print(f"Обработка файла из {file_1.file_path} в потоке {current_thread().name}")
    # Просто имитация сложных вычислений
    _ = [i for i in range(100_000_000)]
    
    encryption_counter += time.perf_counter() - start_timer

# Задача с блокировкой ввода/вывода (загрузка изображения по URL)
def download_image(image_url, file_2: File):
    global download_counter
    start_timer = time.perf_counter()
    print(f"Загрузка изображения по адресу {image_url} в потоке {current_thread().name}")
    response = requests.get(image_url)
    file_2.file.write(response.content)
   
    download_counter += time.perf_counter() - start_timer    

def using_threads(file_1: File, file_2: File):
    threads = [
        Thread(target=encrypt_file, args=(file_1,)),
        Thread(target=download_image, args=("https://picsum.photos/1000/1000", file_2)),
    ]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()

if __name__ == "__main__":
    
    file_1 = File("rockyou.txt", "wb")
    file_2 = File("image.jpg", "wb")

    try:
        start = time.perf_counter()
        using_threads(file_1, file_2)
        total = time.perf_counter() - start
        file_1.close()
        file_2.close()
        
        print(f"Затраченное время на задачу с вычислениями: {encryption_counter}, задачу с вводом/выводом: {download_counter}, Всего: {total} секунд")
    except Exception as e:
        print(f"Произошла ошибка: {e}")
