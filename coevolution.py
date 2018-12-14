# Copywrite James Kayes © 2018
import pygame
import random
from species import *

prey_colour = (128, 0, 0)
predator_colour = (255, 0, 255)
food_colour = (0, 255, 0)
block_colour = (100, 100, 100)
pygame.init()

gameDisplay = pygame.display.set_mode((800,600))
pygame.display.set_caption('Coevolution')
window_icon = pygame.image.load('icon.png')
pygame.display.set_icon(window_icon)

gameExit = False

world = []
x = 0
for x_pos in range(0, 800, 10):
    world.append([])
    for y_pos in range(0, 600, 10):
        # Boundry:
        if(y_pos == 0 or x_pos == 0 or y_pos == 590 or x_pos == 790):
            world[x].append('Block')
        else:
            if(random.random() < 0.15):
                world[x].append('Block')
            else:
                world[x].append('Empty')
    x += 1

for x_pos in range(len(world)):
    for y_pos in range(len(world[0])):
        if(world[x_pos][y_pos] == 'Block'):
            x = x_pos*10
            y = y_pos*10
            pygame.draw.rect(gameDisplay, block_colour, [x, y, 10, 10])

while not gameExit:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            gameExit = True

    pygame.display.update()
    
pygame.quit()
quit()