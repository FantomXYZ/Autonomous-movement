import pygame
import random
import math

# Параметры окна Pygame
CAR_SIZE = 20
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
BG_COLOR = (255, 255, 255)
bg = (0, 255, 0)

SIDE_SIZE = 20

IMAGE_WIDTH = 1000
IMAGE_HEIGHT = 600


class Car2:
    def __init__(self):
        # Начальные параметры автомобиля
        self.speed = 5
        self.radars = []
        self.is_alive = True
        self.distance = 0
        self.pos = [100, 500]
        self.compute_center()
        self.color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        self.history = []
        self.dir = 0
        self.angle = 0
        self.time = 0
        self.way_time = 1000
        self.is_finished = False
        self.positions = []
        self.v_hist = []

    def compute_center(self):
        # Вычисление центра автомобиля
        self.center = (self.pos[0] + (CAR_SIZE / 2), self.pos[1] + (CAR_SIZE / 2))

    def draw_center(self, screen):
        # Отрисовка центра автомобиля
        self.compute_center()
        pygame.draw.circle(screen, (0, 72, 186), (math.floor(self.center[0]), math.floor(self.center[1])), 3)

    def is_live(self, trace):
        # Проверка состояния автомобиля (выжил или нет)
        if trace.get_at(self.radars[5][0]) == bg or trace.get_at(self.radars[6][0]) == bg or trace.get_at(
                self.radars[7][0]) == bg:
            self.is_alive = False
        elif trace.get_at(self.radars[5][0]) == (255, 0, 0):
            self.is_finished = True
            self.is_alive = False

    def compute_radars(self, trace):
        # Вычисление радаров для обнаружения препятствий
        self.radars.clear()
        arr_x_1 = 0
        arr_y_1 = 0
        arr_x_2 = 0
        arr_y_2 = 0
        arr_x_3 = 0
        arr_y_3 = 0
        self.compute_center()
        for degree in [0, -45, 45, -90, 90]:
            length = 0
            x = int(self.center[0] - math.sin(math.radians(degree + self.angle)) * length)
            y = int(self.center[1] - math.cos(math.radians(degree + self.angle)) * length)

            while not trace.get_at((x, y)) == bg and length < 200:
                length += 1
                x = int(self.center[0] - math.sin(math.radians(360 - (degree + self.angle))) * length)
                y = int(self.center[1] - math.cos(math.radians(360 - (degree + self.angle))) * length)

            if degree == 0:
                arr_x_1 = int(self.center[0] - math.sin(math.radians(360 - (degree + self.angle))) * 30)
                arr_y_1 = int(self.center[1] - math.cos(math.radians(360 - (degree + self.angle))) * 30)
            elif degree == 90:
                arr_x_2 = int(self.center[0] - math.sin(math.radians(360 - (degree + self.angle))) * 15)
                arr_y_2 = int(self.center[1] - math.cos(math.radians(360 - (degree + self.angle))) * 15)
            elif degree == -90:
                arr_x_3 = int(self.center[0] - math.sin(math.radians(360 - (degree + self.angle))) * 15)
                arr_y_3 = int(self.center[1] - math.cos(math.radians(360 - (degree + self.angle))) * 15)

            dist = int(math.sqrt(math.pow(x - self.center[0], 2) + math.pow(y - self.center[1], 2)))

            self.radars.append([(x, y), dist])
        self.radars.append([(arr_x_1, arr_y_1), dist])
        self.radars.append([(arr_x_2, arr_y_2), dist])
        self.radars.append([(arr_x_3, arr_y_3), dist])

    def draw_radars(self, screen):
        # Отрисовка радаров
        for r in self.radars[:5]:
            p, d = r
            pygame.draw.line(screen, (255, 0, 0), self.center, p, 1)
            pygame.draw.circle(screen, (183, 235, 70), p, 5)

    def draw(self, screen):
        # Отрисовка автомобиля и радаров
        p1, _ = self.radars[5]
        p2, _ = self.radars[6]
        p3, _ = self.radars[7]
        pygame.draw.polygon(screen, self.color, [p1, p2, p3])

        self.draw_center(screen)
        self.draw_radars(screen)

    def get_data(self):
        # Получение данных от радаров и текущей скорости
        radars = self.radars
        data = [0, 0, 0, 0, 0, 0]

        for i, r in enumerate(radars[:5]):
            data[i] = int(r[1] / 30)

        data[5] = self.speed

        return data

    def get_reward(self):
        # Получение вознаграждения
        if self.is_finished:
            return self.distance + self.distance * 1000 / self.time
        return self.distance
