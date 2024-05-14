from tkinter import *
from traning import Traning 
import os

class GenSelector:
    
    def __init__(self, root, image_path, is_uniform, is_slow):
        # Инициализация объекта GenSelector с корневым окном, путем к изображению и параметрами тренировки
        self.root = root
        self.image_path = image_path
        self.is_uniform = is_uniform
        self.is_slow = is_slow
        
    def start_new(self, window):
        # Запуск новой тренировки без использования сохраненных параметров
        window.withdraw()
        training = Traning(self.image_path, self.is_uniform, self.is_slow, is_new=True, p_path="")
        
    def start(self, window, path):
        # Запуск тренировки с использованием сохраненных параметров
        window.withdraw()
        training = Traning(self.image_path, self.is_uniform, self.is_slow, is_new=False, p_path=path)
    
    def run(self):
        # Запуск процесса выбора тренировки
        self.root.withdraw()
        new_window = Toplevel()
        new_window.title("Select Trace")
        new_window.protocol("WM_DELETE_WINDOW", self.root.quit)
        
        # Кнопка для запуска новой тренировки
        new_button = Button(new_window, text="Новое поколение", command=lambda: self.start_new(new_window), font=("Arial", 14))
        new_button.pack()
        
        # Определение пути к папке с сохраненными параметрами тренировки
        folder_path = "checkpoints/uniform" if self.is_uniform else "checkpoints/equidistant"
        
        # Получение списка файлов с сохраненными параметрами тренировки
        p_files = [os.path.join(folder_path, file_name) for file_name in os.listdir(folder_path)]
        
        # Создание кнопок для запуска тренировки с использованием сохраненных параметров
        for i, p_file in enumerate(p_files):
            gen = p_file.split("_")[-1]  # Получение номера поколения из имени файла
            Button(new_window, text=f"{i+1}. Поколений обучения: {gen}", command=lambda p=p_file: self.start(new_window, p), font=("Arial", 14)).pack()
