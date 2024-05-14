import tkinter as tk
from PIL import Image, ImageTk
from tkinter import Toplevel, Listbox, Scrollbar
import sys

class DataViewer:
    
    def __init__(self, trace, data):
        # Инициализация объекта DataViewer с данными и путем к изображению
        self.data_index = 0
        self.data = sorted(data, key=lambda x: x[0], reverse=True)  # Сортировка данных по пройденному расстоянию
        self.image_path = trace
        
    def run(self):
        # Запуск отображения данных
        self.create_window()
        
    def create_window(self):
        # Создание окна для отображения данных
        self.new_window = Toplevel()

        self.display_info()  # Отображение информации о данных

        prev_button = tk.Button(self.new_window, text="Назад", command=self.prev_data)
        prev_button.pack(side=tk.TOP)

        next_button = tk.Button(self.new_window, text="Вперёд", command=self.next_data)
        next_button.pack(side=tk.TOP)
        
        self.new_window.protocol("WM_DELETE_WINDOW", self.hide_window)  # Обработка закрытия окна

        self.new_window.mainloop()
        
    def display_info(self):
        # Отображение информации о данных
        data_info = self.data[self.data_index]
        
        # Загрузка изображения и создание объекта PhotoImage для отображения на Canvas
        self.image = Image.open(self.image_path)
        self.photo = ImageTk.PhotoImage(self.image)
        canvas = tk.Canvas(self.new_window, width=self.image.width, height=self.image.height)
        canvas.create_image(0, 0, anchor=tk.NW, image=self.photo)
        
        # Отрисовка траектории движения на изображении
        points = data_info[2]
        for i in range(len(points) - 1):
            x1, y1 = points[i]
            x2, y2 = points[i+1]
            canvas.create_line(x1, y1, x2, y2, fill="red", width=2)
        
        canvas.pack(side=tk.LEFT)
        
        # Отображение информации о пройденном расстоянии, времени и координатах
        car_info = tk.Label(self.new_window, text=f"Машинка № {self.data_index}")
        car_info.pack()
        
        distance_label = tk.Label(self.new_window, text=f"Пройденное расстояние: {data_info[0]}")
        distance_label.pack()

        time_label = tk.Label(self.new_window, text=f"Время: {data_info[1]}")
        time_label.pack()

        # Создание списка координат и добавление прокрутки
        scrollbar = Scrollbar(self.new_window, orient=tk.VERTICAL)
        coordinates_list = Listbox(self.new_window, yscrollcommand=scrollbar.set)
        for point in data_info[3]:
            coordinates_list.insert(tk.END, point)
        coordinates_list.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=coordinates_list.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
    def next_data(self):
        # Переход к следующим данным
        self.data_index = (self.data_index + 1) % len(self.data)
        self.new_window.destroy()
        self.create_window()

    def prev_data(self):
        # Переход к предыдущим данным
        self.data_index = (self.data_index - 1) % len(self.data)
        self.new_window.destroy()
        self.create_window()
        
    def hide_window(self):
        # Закрытие окна
        sys.exit(0)  # Выход из приложения
