import pygame
import os

WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 600
BG_COLOR = (0, 255, 0)
DRAW_COLOR = (255, 255, 255)
DRAW_SIZE = 35

SAVE_FOLDER = "traces"  # Имя папки для сохранения изображений

class TraceCreator:
    
    def __init__(self):
        pass
    
    def run(self):
        # Инициализация Pygame и создание окна
        pygame.init()
        window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Paint")

        drawing = False  # Переменная для отслеживания рисования
        screen = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))  # Создание поверхности для рисования
        screen.fill(BG_COLOR)  # Заполнение экрана цветом заднего фона
        pygame.draw.rect(screen, (255, 0, 0), (100, 500, 20, 20))  # Рисование прямоугольника на экране

        clock = pygame.time.Clock()  # Создание объекта Clock для управления FPS

        while True:
            for event in pygame.event.get():  # Обработка событий
                if event.type == pygame.QUIT:  # Закрытие окна
                    pygame.quit()
                    return
                elif event.type == pygame.MOUSEBUTTONDOWN:  # Обработка нажатия кнопки мыши
                    if event.button == 1:  # Левая кнопка мыши
                        drawing = True
                elif event.type == pygame.MOUSEBUTTONUP:  # Обработка отпускания кнопки мыши
                    if event.button == 1:
                        drawing = False
                elif event.type == pygame.MOUSEMOTION:  # Обработка движения мыши
                    if drawing:
                        pos = pygame.mouse.get_pos()
                        pygame.draw.circle(screen, DRAW_COLOR, pos, DRAW_SIZE)  # Рисование круга на экране
                elif event.type == pygame.KEYDOWN:  # Обработка нажатия клавиши
                    if event.key == pygame.K_s:  # Клавиша 's' для сохранения изображения
                        self.save_image(screen)
                    elif event.key == pygame.K_r:  # Клавиша 'r' для рисования красного круга
                        pos = pygame.mouse.get_pos()
                        pygame.draw.circle(screen, (255, 0, 0), pos, DRAW_SIZE)

            window.blit(screen, (0, 0))  # Отображение поверхности на экране
            pygame.display.flip()  # Обновление экрана
            clock.tick(60)  # Ограничение FPS

    def save_image(self, surface):
        if not os.path.exists(SAVE_FOLDER):  # Проверка наличия папки для сохранения изображений
            os.makedirs(SAVE_FOLDER)  # Создание папки, если ее нет
        image_count = len(os.listdir(SAVE_FOLDER))  # Получение количества существующих изображений
        image_path = os.path.join(SAVE_FOLDER, f"trace_{image_count}.png")  # Формирование пути к новому изображению
        pygame.image.save(surface, image_path)  # Сохранение изображения
        print(f"Изображение сохранено: {image_path}")  # Вывод сообщения о сохранении
