from typing import Self
import pygame
import numpy as np
from tkinter import Tk, filedialog
import math
import random
import neat
import sys

CAR_COUNT = 27
CAR_SIZE = 20
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
BG_COLOR = (255, 255, 255)
bg = (0, 255, 0)

IMAGE_WIDTH = 1000
IMAGE_HEIGHT = 600


def main():
    pygame.init()
    window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Dialog Window")

    clock = pygame.time.Clock()
    
    
    window.fill(BG_COLOR)
    draw_button(window)
    draw_newai_button(window)
    draw_proai_button(window)
    pygame.display.flip()
    clock.tick(60)
    image_path = ""
    while True:
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    # Открытие диалогового окна для выбора картинки
                    if button_rect.collidepoint(event.pos):
                        image_path = select_image()
                    # Нажатие кнопки "newAI"
                    if newai_button_rect.collidepoint(event.pos):
                        print(image_path)
                        if image_path != "":
                            open_image_window(image_path)
                    # Нажатие кнопки "proAI"
                    if proai_button_rect.collidepoint(event.pos):
                        if image_path != "":
                            open_image_window(image_path)
        
def draw_button(surface):
    global button_rect
    button_font = pygame.font.SysFont(None, 30)
    button_text = button_font.render("Выбрать картинку", True, (0, 0, 0))
    button_rect = button_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 50))
    pygame.draw.rect(surface, (200, 200, 200), button_rect)
    surface.blit(button_text, button_rect)

def draw_newai_button(surface):
    global newai_button_rect
    button_font = pygame.font.SysFont(None, 30)
    button_text = button_font.render("newAI", True, (0, 0, 0))
    newai_button_rect = button_text.get_rect(center=(WINDOW_WIDTH // 2 - 100, WINDOW_HEIGHT // 2 + 50))
    pygame.draw.rect(surface, (200, 200, 200), newai_button_rect)
    surface.blit(button_text, newai_button_rect)

def draw_proai_button(surface):
    global proai_button_rect
    button_font = pygame.font.SysFont(None, 30)
    button_text = button_font.render("proAI", True, (0, 0, 0))
    proai_button_rect = button_text.get_rect(center=(WINDOW_WIDTH // 2 + 100, WINDOW_HEIGHT // 2 + 50))
    pygame.draw.rect(surface, (200, 200, 200), proai_button_rect)
    surface.blit(button_text, proai_button_rect)

def select_image():
    root = Tk()
    root.withdraw()
    image_path = filedialog.askopenfilename(title="Выберите картинку", filetypes=[("Изображения", "*.png;*.jpg;*.jpeg")])
    return image_path


class Car():
    def __init__(self):
        self.speed = 5
        self.radars = []
        self.is_alive = True
        self.distance = 0
        self.pos = [100, 500]
        self.compute_center()
        self.color = (random.randint(0,255),random.randint(0,255),random.randint(0,255))
        self.history = []
        self.history.append(0)
        self.dir = 0
        self.angle = 0 
		

    def compute_center(self):
        self.center = (self.pos[0] + (CAR_SIZE / 2), self.pos[1] + (CAR_SIZE / 2))
  
  
    def draw_center(self, screen):
        self.compute_center()
        pygame.draw.circle(screen, (0, 72, 186), (math.floor(self.center[0]), math.floor(self.center[1])), 3)

	
    def is_live(self,trace):
        if trace.get_at((self.pos[0], self.pos[1])) == bg or trace.get_at((self.pos[0]+CAR_SIZE, self.pos[1]+CAR_SIZE)) == bg:
            self.is_alive = False
	
	
    def compute_radars(self, trace):
        self.radars.clear()
        for degree in [0,-45,45,-90,90]:
            length = 0
            x = int(self.center[0] - math.sin(math.radians(degree + self.angle)) * length)
            y = int(self.center[1] - math.cos(math.radians(degree + self.angle)) * length)
				

            while not trace.get_at((x, y)) == bg and length < 300:
                length = length + 1
                x = int(self.center[0] - math.sin(math.radians(360 - (degree + self.angle))) * length)
                y = int(self.center[1] - math.cos(math.radians(360 - (degree + self.angle))) * length)
					
					


            dist = int(math.sqrt(math.pow(x - self.center[0], 2) + math.pow(y - self.center[1], 2)))
            
            self.radars.append([(x, y), dist])
		
  
  
    def draw_radars(self,screen):
		
        for r in self.radars:
            p, d = r
            pygame.draw.line(screen,(255,0,0),self.center,p,1)
            pygame.draw.circle(screen, (183,235,70), p, 5)



    def draw(self, screen):
        pygame.draw.rect(screen,self.color,(self.pos[0],self.pos[1],20,20))
        self.draw_center(screen)
        
        self.draw_radars(screen)
		

    def get_data(self):
        radars = self.radars
        data = [0, 0, 0, 0, 0]

        for i, r in enumerate(radars):
            data[i] = int(r[1] / 30)

        return data

    def get_reward(self):
        return self.distance / 50.0




def run_generation(genomes, config):
    nets = []
    cars = []
    image_path = "traces/trace_5.png"
    # init genomes
    for i, g in genomes:
        net = neat.nn.FeedForwardNetwork.create(g, config)
        nets.append(net)
        g.fitness = 0 # every genome is not successful at the start

        # init cars
        cars.append(Car())
    
    
    pygame.init()
    screen = pygame.display.set_mode((IMAGE_WIDTH, IMAGE_HEIGHT))
    pygame.display.set_caption("Window")
    image = pygame.image.load(image_path)
    image = pygame.transform.scale(image, (IMAGE_WIDTH, IMAGE_HEIGHT))
    
    clock = pygame.time.Clock()
    game_over = False
    
    
    while True:
     
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit(0)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    start = True


		# input each car data
        for i, car in enumerate(cars):
            output = nets[i].activate(car.get_data())
            i = output.index(max(output))

            if i == 0:
                car.angle += 5
            elif i == 1:
                car.angle = car.angle
            elif i == 2:
                car.angle -= 5

		# now, update car and set fitness (for alive cars only)
        cars_left = 0
        for i, car in enumerate(cars):
            car.is_live(image)
            if car.is_alive:
                cars_left += 1
                
                car.pos[0] -= math.sin(math.radians(360 - car.angle)) * car.speed
                car.pos[1] -= math.cos(math.radians(360 - car.angle)) * car.speed
                
                car.distance += car.speed
                
                genomes[i][1].fitness += car.get_reward() # new fitness (aka car instance success)

		# check if cars left
        if not cars_left:
            break

		# display stuff
        screen.blit(image, (0, 0))

        
        
        for car in cars:
            if car.is_alive:
                car.compute_radars(image)
                car.draw(screen)

        

        pygame.display.flip()
        clock.tick(110)
    
    
    


def open_image_window(image_path):
    pygame.quit()
    # setup config
    config_path = "./config-feedforward.txt"
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction, neat.DefaultSpeciesSet, neat.DefaultStagnation, config_path)
    p = neat.Population(config)
    p.run(run_generation, 1000)
    
    

if __name__ == "__main__":
    main()