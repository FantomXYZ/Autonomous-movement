import tkinter as tk
from traceSelector import TraceSelector
from traceCreator import TraceCreator

def start_train(root, is_uniform, is_slow):
    """Функция для запуска тренировки с заданными параметрами."""
    selector = TraceSelector(root, is_uniform, is_slow)
    selector.run()

def create_new_trace():
    """Функция для создания новой трассы."""
    creator = TraceCreator()
    creator.run()

def main():
    # Создаем основное окно
    root = tk.Tk()
    root.title("CarAI")  # Заголовок окна

    # Создаем и размещаем виджеты для равномерного движения
    label_uniform = tk.Label(root, text="Равномерное движение", font=("Arial", 16))
    label_uniform.pack()
    button_uniform_fast = tk.Button(root, text="Быстрая тренировка", command=lambda: start_train(root, is_uniform=True, is_slow=False), font=("Arial", 14))
    button_uniform_fast.pack()
    button_uniform_slow = tk.Button(root, text="Медленная тренировка", command=lambda: start_train(root, is_uniform=True, is_slow=True), font=("Arial", 14))
    button_uniform_slow.pack()

    # Создаем и размещаем виджеты для равноускоренного движения
    label_non_uniform = tk.Label(root, text="Равноускоренное движение", font=("Arial", 16))
    label_non_uniform.pack()
    button_non_uniform_fast = tk.Button(root, text="Быстрая тренировка", command=lambda: start_train(root, is_uniform=False, is_slow=False), font=("Arial", 14))
    button_non_uniform_fast.pack()
    button_non_uniform_slow = tk.Button(root, text="Медленная тренировка", command=lambda: start_train(root, is_uniform=False, is_slow=True), font=("Arial", 14))
    button_non_uniform_slow.pack()

    # Создаем и размещаем виджет для создания новой трассы
    label_new_trace = tk.Label(root, text="Новая трасса", font=("Arial", 16))
    label_new_trace.pack()
    button_create_new_trace = tk.Button(root, text="Создать", command=create_new_trace, font=("Arial", 14))
    button_create_new_trace.pack()

    # Запускаем главный цикл обработки событий
    root.mainloop()

if __name__ == "__main__":
    main()
