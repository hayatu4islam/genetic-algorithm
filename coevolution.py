# Copywrite James Kayes © 2018
import pygame
import random
import itertools
from species import *
from gene_functions import *

prey_colour = (255, 0, 0)
predator_colour = (255, 0, 255)
food_colour = (0, 255, 0)
block_colour = (100, 100, 100)
world = []
prey_list = []
predator_list = []
food_list = []

# These will hold a list of dictionaries with 2 entries: The specimens genes and its fitness:
prey_genes = []
predator_genes = [] 

prey_count = 200
predator_count = 75
food_count = 100

resolution = {'x': 1020, 'y': 800}
# Sets the initial world up with the boundary and a random set of boundary blocks:
def new_board():
    world.clear()
    x = 0
    for x_position in range(0, resolution['x'], 10):
        world.append([])
        for y_position in range(0, resolution['y'], 10):
            # Boundry:
            if(y_position == 0 or x_position == 0 or y_position == (resolution['y']-10) or x_position == (resolution['x']-10)):
                pygame.draw.rect(gameDisplay, block_colour, [x_position, y_position, 10, 10])
                world[x].append('Block')
            else:
                if(random.random() < 0.15):
                    pygame.draw.rect(gameDisplay, block_colour, [x_position, y_position, 10, 10])
                    world[x].append('Block')
                else:
                    pygame.draw.rect(gameDisplay, (0,0,0), [x_position, y_position, 10, 10])
                    world[x].append('Empty')
        x += 1

def spawn_life():
    world_width = len(world)-1
    world_height = len(world[0])-1

    for food in range(food_count):
        random_x = random.randint(0, world_width)
        random_y = random.randint(0, world_height)
        while(world[random_x][random_y] != 'Empty'):
            random_x = random.randint(0, world_width)
            random_y = random.randint(0, world_height)
        world[random_x][random_y] = 'Food'
        food_list.append((random_x, random_y, False))

    for prey_index in range(prey_count):
        random_x = random.randint(0, world_width)
        random_y = random.randint(0, world_height)
        while(world[random_x][random_y] != 'Empty'):
            random_x = random.randint(0, world_width)
            random_y = random.randint(0, world_height)
        world[random_x][random_y] = 'Prey'
        prey_list.append(Prey(prey_genes[prey_index]['genes'], (random_x, random_y), 'N'))

    for predator_index in range(predator_count):
        random_x = random.randint(0, world_width)
        random_y = random.randint(0, world_height)
        while(world[random_x][random_y] != 'Empty'):
            random_x = random.randint(0, world_width)
            random_y = random.randint(0, world_height)
        world[random_x][random_y] = 'Predator'
        predator_list.append(Predator(predator_genes[predator_index]['genes'], (random_x, random_y), 'N'))
        
# Clear block at this position:
def clear(position):
    pygame.draw.rect(gameDisplay, (0,0,0), [position[0]*10, position[1]*10, 10, 10])
    world[position[0]][position[1]] = 'Empty'

def draw_world():
    for prey in prey_list:
        if(not prey.dead):
            pygame.draw.rect(gameDisplay, prey_colour, [prey.x_position*10, prey.y_position*10, 10, 10])

    for predator in predator_list:
        if(not predator.dead):
            pygame.draw.rect(gameDisplay, predator_colour, [predator.x_position*10, predator.y_position*10, 10, 10])

    for item in food_list:
        x_position, y_position, eaten = item
        if(not eaten):
            pygame.draw.rect(gameDisplay, food_colour, [x_position*10, y_position*10, 10, 10])

def update():
    for food_x, food_y, food_eaten in food_list:
        if(food_eaten == True):
            clear((food_x, food_y))
            food_list.remove((food_x, food_y, food_eaten))

    for prey in prey_list:
        clear((prey.x_position, prey.y_position))
        if(not prey.dead):
            prey.update_state(world)
            prey.take_action(food_list)
            # Update world:
            world[prey.x_position][prey.y_position] = 'Prey'
        else:
            # Add fitness to genes: 
            for specimen in prey_genes:
                if(specimen['genes'] == prey.genes):
                    # Fitness is the age at death + added fitness dependent on when it catches food, this is to encourage more interesting behaviour:
                    specimen['fitness'] = prey.fitness
            world[prey.x_position][prey.y_position] = 'Empty'
            prey_list.remove(prey)

    for predator in predator_list:
        clear((predator.x_position, predator.y_position))
        if(not predator.dead):
            predator.update_state(world)
            predator.take_action(prey_list)
            # Update world:
            world[predator.x_position][predator.y_position] = 'Predator'
        else:
            # Add fitness to genes: 
            for specimen in predator_genes:
                if(specimen['genes'] == predator.genes):
                    specimen['fitness'] = predator.fitness
            world[predator.x_position][predator.y_position] = 'Empty'
            predator_list.remove(predator)

def initiaise_genes(count, genome_length=3125, max_gene=9):
    genes_list = []
    for i in range(count):
        genes_list.append({'genes': [], 'fitness': None})
        for gene in range(genome_length):
            genes_list[i]['genes'].append(random.randint(0, max_gene))
    return genes_list

def draw_blockades():
    # Draw blockades, we only need to do this once as they don't change positions:
    for x_pos in range(len(world)):
        for y_pos in range(len(world[0])):
            if(world[x_pos][y_pos] == 'Block'):
                x = x_pos*10
                y = y_pos*10
                pygame.draw.rect(gameDisplay, block_colour, [x, y, 10, 10])


pygame.init()

gameDisplay = pygame.display.set_mode((resolution['x'],resolution['y']))
pygame.display.set_caption('Coevolution')
window_icon = pygame.image.load('icon.png')
pygame.display.set_icon(window_icon)

gameExit = False

x = 0
prey_genes = initiaise_genes(prey_count)
predator_genes = initiaise_genes(predator_count)

new_board()
draw_blockades()
spawn_life()

# Game loop:
generation = 1
steps = 0
while not gameExit:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            gameExit = True
    
    # New generation:
    if(len(prey_list) == 0 and len(predator_list) == 0): 
        steps = 0
        print('\nGeneration ' + str(generation) + ' complete')
        print('Applying crossover/mutation with rank based selection to generate new genes')
        # Genes sorted by fitness:
        sorted_prey_genes = sorted(prey_genes, key = lambda item: item['fitness'], reverse=True)
        sorted_predator_genes = sorted(predator_genes, key = lambda item: item['fitness'], reverse=True)
        for prey_index in range(len(prey_genes)):
            # Select acording to rank based selection, remove from the list to prevent breeding with itself to increase gene diversity:
            a_rank = rank_based_selection(sorted_prey_genes)
            prey_dict = sorted_prey_genes.pop(a_rank)
            prey_genes_a = prey_dict['genes']
            # Getting the rank for the second parent from the remaining genes:
            prey_genes_b = sorted_prey_genes[rank_based_selection(sorted_prey_genes)]['genes']
            # Crossover applied to create a new set of genes for the next generation:
            prey_genes[prey_index]['genes'] = mutate(crossover(prey_genes_a, prey_genes_b))
            
            # Re-inserting removed genes in the correct place:
            sorted_prey_genes.insert(a_rank, prey_dict)

        for predator_index in range(len(predator_genes)):
            # Select rank acording to rank based selection, and remove from the list to prevent breeding with itself to increase gene diversity:
            a_rank = rank_based_selection(sorted_predator_genes)
            predator_dict = sorted_predator_genes.pop(a_rank)
            predator_genes_a = predator_dict['genes']
            # Getting the rank for the second parent from the remaining genes:
            predator_genes_b = sorted_predator_genes[rank_based_selection(sorted_predator_genes)]['genes']

            # Crossover and mutation applied to create a new set of genes for the next generation:
            predator_genes[predator_index]['genes'] = mutate(crossover(predator_genes_a, predator_genes_b))

            # Re-inserting removed genes in the correct place:
            sorted_predator_genes.insert(a_rank, predator_dict)
        generation += 1
        food_list.clear()
        new_board()
        draw_blockades()
        spawn_life()

    update()
    steps += 1
    if(steps%1000 == 0 or steps == 0):
        print('After step: {}, Food: {}, Prey: {}, Predators: {}'.format(steps, len(food_list), len(prey_list), len(predator_list)))
    draw_world()
    pygame.display.update()
    
pygame.quit()
quit()