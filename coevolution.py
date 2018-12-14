# Copywrite James Kayes © 2018
import pygame
import random
from species import *

prey_colour = (255, 0, 0)
predator_colour = (255, 0, 255)
food_colour = (0, 255, 0)
block_colour = (100, 100, 100)

def spawn_blocks(world):
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

def spawn_objects(world, pred_list, prey_list, food_count=100, prey_count=20, predator_count=10):
    world_width = len(world)-1
    world_height = len(world[0])-1

    for food in range(food_count):
        random_x = random.randint(0, world_width)
        random_y = random.randint(0, world_height)
        while(world[random_x][random_y] != 'Empty'):
            random_x = random.randint(0, world_width)
            random_y = random.randint(0, world_height)
        world[random_x][random_y] = 'Food'
        food_list.append((random_x, random_y))

    for prey in range(prey_count):
        random_x = random.randint(0, world_width)
        random_y = random.randint(0, world_height)
        while(world[random_x][random_y] != 'Empty'):
            random_x = random.randint(0, world_width)
            random_y = random.randint(0, world_height)
        world[random_x][random_y] = 'Prey'
        prey_list.append(Prey((random_x, random_y), 'N'))
    
    for predator in range(predator_count):
        random_x = random.randint(0, world_width)
        random_y = random.randint(0, world_height)
        while(world[random_x][random_y] != 'Empty'):
            random_x = random.randint(0, world_width)
            random_y = random.randint(0, world_height)
        world[random_x][random_y] = 'Predator'
        pred_list.append(Predator((random_x, random_y), 'N'))

def clear_world():
    for prey in prey_list:
        pygame.draw.rect(gameDisplay, (0,0,0), [prey.x_position*10, prey.y_position*10, 10, 10])
    for predator in predator_list:
        pygame.draw.rect(gameDisplay, (0,0,0), [predator.x_position*10, predator.y_position*10, 10, 10])
    for x_position, y_position in food_list:
        pygame.draw.rect(gameDisplay, (0,0,0), [x_position*10, y_position*10, 10, 10])

def draw_world():
    for prey in prey_list:
        pygame.draw.rect(gameDisplay, prey_colour, [prey.x_position*10, prey.y_position*10, 10, 10])
    for predator in predator_list:
        pygame.draw.rect(gameDisplay, predator_colour, [predator.x_position*10, predator.y_position*10, 10, 10])
    for x_position, y_position in food_list:
        pygame.draw.rect(gameDisplay, food_colour, [x_position*10, y_position*10, 10, 10])

pygame.init()

gameDisplay = pygame.display.set_mode((800,600))
pygame.display.set_caption('Coevolution')
window_icon = pygame.image.load('icon.png')
pygame.display.set_icon(window_icon)

gameExit = False

world = []
prey_list = []
predator_list = []
food_list = []
x = 0
spawn_blocks(world)
spawn_objects(world, predator_list, prey_list)
# Draw blocks, we only need to do this once as they don't change positions:
for x_pos in range(len(world)):
    for y_pos in range(len(world[0])):
        if(world[x_pos][y_pos] == 'Block'):
            x = x_pos*10
            y = y_pos*10
            pygame.draw.rect(gameDisplay, block_colour, [x, y, 10, 10])

# Game loop:
while not gameExit:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            gameExit = True

    clear_world()

    draw_world()
    pygame.display.update()
    
pygame.quit()
quit()