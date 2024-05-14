from tkinter import *
from PIL import Image, ImageTk
import os
from genSelection import GenSelector  

class TraceSelector:
    
    def __init__(self, root, is_uniform, is_slow):
        self.root = root
        self.is_uniform = is_uniform
        self.is_slow = is_slow
        
    def start_gen_selection(self, root, image_path):
        gen_selector = GenSelector(root, image_path, self.is_uniform, self.is_slow)
        gen_selector.run()
    
    def run(self):
        # Скрыть основное окно
        self.root.withdraw()
        
        # Создать новое окно
        new_window = Toplevel()
        new_window.title("Select Trace")
        new_window.protocol("WM_DELETE_WINDOW", self.root.quit)  # Закрыть основное окно при закрытии нового
        
        # Получить список файлов изображений
        image_files = self.get_image_files("traces")
        
        j = 0
        for i in range(len(image_files)):
            # Открыть изображение с помощью PIL и изменить размер
            image = Image.open(image_files[i])
            image = image.resize((200, 125))
            photo = ImageTk.PhotoImage(image)
            
            # Создать кнопку с изображением
            button = Button(new_window, image=photo, command=lambda image_file=image_files[i]: self.start_gen_selection(new_window, image_file))
            button.image = photo
            
            # Разместить кнопку на сетке
            if i % 5 != 0:
                button.grid(row=j, column=i % 5)
            else:
                j += 1
                button.grid(row=j, column=i % 5)
        
    def get_image_files(self, folder_path):
        # Получить список файлов изображений в заданной папке
        image_files = []
        for file_name in os.listdir(folder_path):
            if file_name.endswith(".jpg") or file_name.endswith(".png"):
                file_path = os.path.join(folder_path, file_name)
                image_files.append(file_path)
        return image_files
