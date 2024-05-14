import neat
from typing import Self
import pygame
import numpy as np
from tkinter import Tk, filedialog
import math
import sys
from car_v2 import Car2
from car import Car
import random
import os
from data_view import DataViewer
import threading
import time

last_time = 1000
WHITE = (255, 255, 255)
CAR_SIZE = 20
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
BG_COLOR = (255, 255, 255)
bg = (0, 255, 0)

a = 1

SIDE_SIZE = 20

IMAGE_WIDTH = 1000
IMAGE_HEIGHT = 600

DISCREATE_SIZE = 1

class Traning():
    
    
    def __init__(self,image_path,is_uniform,is_slow,is_new,p_path):
        
       
        
        self.is_uniform = is_uniform
        self.is_slow = is_slow
        self.image_path = image_path
        self.is_slow = is_slow
        self.generation = 0
        self.best_time = ""
        self.is_finished = False
        self.history = []
        self.best_v = []
        
        config_path = ""
        
        if is_new:
            if is_uniform:
                config_path = "./config-feedforward1.txt"
            else:
                config_path = "./config-feedforward2.txt"
                
            random.seed(42)
            config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction, neat.DefaultSpeciesSet, neat.DefaultStagnation, config_path)
            p = neat.Population(config)
        else:
            p = neat.Checkpointer.restore_checkpoint(p_path)
            self.generation = int(p_path.split("_")[-1])
         
        self.p = p
        p.run(self.run_generation, 1000)
    
    def run_generation(self, genomes, config):
        nets = []
        cars = []
        image_path = self.image_path
        
        
        for _, g in genomes:
            net = neat.nn.FeedForwardNetwork.create(g, config)
            nets.append(net)
            g.fitness = 0
            if self.is_uniform:
                cars.append(Car())
            else:
                cars.append(Car2())
                
        image = pygame.image.load(image_path)
        image = pygame.transform.scale(image, (IMAGE_WIDTH, IMAGE_HEIGHT))
        
        if self.is_slow or self.is_finished:
            pygame.init()
            screen = pygame.display.set_mode((IMAGE_WIDTH, IMAGE_HEIGHT + 50))
            pygame.display.set_caption("CarAI")
            clock = pygame.time.Clock()
    
        while True:
            if self.is_slow or self.is_finished:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        print(self.best_v)
                        sys.exit(0)
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_s:
                            if self.is_uniform:
                                file_count = len(os.listdir('checkpoints/uniform'))
                                checkpoint = neat.Checkpointer(filename_prefix=f'checkpoints/uniform/population_{file_count}_')
                                checkpoint.save_checkpoint(self.p.config,self.p.population,self.p.species,self.p.generation)
                            else:
                                file_count = len(os.listdir('checkpoints/equidistant'))
                                checkpoint = neat.Checkpointer(filename_prefix=f'checkpoints/equidistant/population_{file_count}_')
                                checkpoint.save_checkpoint(self.p.config,self.p.population,self.p.species,self.p.generation)
                        elif event.key == pygame.K_v:
                            
                            view = DataViewer(self.image_path,self.history)
                            view.create_window()
                            time.sleep(0.1)
                            

            # input each car data
            for i, car in enumerate(cars):
                car.compute_radars(image)
                car.is_live(image)
                if car.is_alive:
                    
                    output = nets[i].activate(car.get_data())
                    
                    car.angle += math.floor(output[0]*10) 
                    
                    if not self.is_uniform:
                        if car.speed + math.floor(output[1]*5) >= 5:
                            car.speed += math.floor(output[1]*5)
                        else:
                            car.speed = 5
                            
                        car.v_hist.append(car.speed)        
                        
                    #car.history.append(to_hist)        

            cars_left = 0
            for i, car in enumerate(cars):
                
                car.compute_radars(image)
                car.is_live(image)
                
                if car.is_alive:
                    cars_left += 1
                    car.positions.append(car.pos.copy())
                    
                    
                    car.pos[0] -= math.sin(math.radians(360 - car.angle)) * car.speed 
                    
                    car.pos[1] -= math.cos(math.radians(360 - car.angle)) * car.speed 
                    
                    car.distance += car.speed 
                    car.time += 1
                    car.positions.append(car.pos.copy())

            
            if cars_left == 0:
                break

            if self.is_slow or self.is_finished:
                screen.blit(image, (0, 0))

                for car in cars:
                    if car.is_alive:
                        car.compute_radars(image)
                        car.draw(screen)
                        
                font = pygame.font.Font(None, 36)
                s = f"Поколение {self.generation}"
                if self.is_uniform == False and self.best_time != "":
                    s += "  Лучшее время: " + self.best_time
                text = font.render(s, True, WHITE)
                text_rect = text.get_rect()
                text_rect.center = (WINDOW_WIDTH // 2, WINDOW_HEIGHT + 25)
                screen.blit(text, text_rect)

                pygame.display.flip()
                clock.tick(120)
            
        
        best = 1000
        
        for i, car in enumerate(cars):
            if car.is_finished:
                
                if best > car.time:
                    best = car.time
                    self.best_v = car.v_hist[:]
                    
                if self.generation == 140:
                    self.is_finished = True
        
        print(best)
        
        
        
        if best != 1000:
            self.best_time = str(best)
        self.generation += 1
        if self.generation % 10 == 0:
            pass
            #print(self.generation)
        
        self.history = []
        
        for car in cars:
            tmp = []
            tmp.append(car.distance)
            tmp.append(car.time)
            tmp.append(car.positions)
            tmp.append(car.history)
            self.history.append(tmp.copy())
            
        for i, car in enumerate(cars):
            genomes[i][1].fitness += car.get_reward()
        
