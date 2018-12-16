from gene_functions import *
import itertools

class Species:
    def __init__(self, genes, position, direction):
        self.x_position, self.y_position = position
        self.state = {}
        self.direction = direction
        self.energy = 50
        self.age = 0
        self.state_action_dict = {} # This is a dictionary from every possible state to the action that should be taken.
        self.genes = genes
        self.state_string = ''
        self.dead = False
        self.fitness = 0

        possible_states = [''.join(item) for item in list(itertools.product('BPYEF', repeat=5))]
        i = 0
        for state in possible_states:
            self.state_action_dict[state] = self.genes[i]
            i += 1

    def build_state_string(self):
        self.state_string = ''
        # Building string acording to state dictionary:
        for key in sorted(self.state.keys()):
            character = 'B'
            if(self.state[key] == 'Empty'):
                character = 'E'
            elif(self.state[key] == 'Predator'):
                character = 'P'
            elif(self.state[key] == 'Prey'):
                character = 'Y'
            elif(self.state[key] == 'Food'):
                character = 'F'
            self.state_string += character

    def move_forward(self):
        if(self.state['F1'] != 'Block'):
            if(self.direction == 'N'):
                self.y_position -= 1
            elif(self.direction == 'E'):
                self.x_position += 1
            elif(self.direction == 'S'):
                self.y_position += 1
            elif(self.direction == 'W'):
                self.x_position -= 1

    def move_left(self):
        if(self.direction == 'N'):
            self.direction = 'W'
            if(self.state['L1'] != 'Block'): 
                self.x_position -= 1
        elif(self.direction == 'E'):
            self.direction = 'N'
            if(self.state['L1'] != 'Block'): 
                self.y_position -= 1
        elif(self.direction == 'S'):
            self.direction = 'E'
            if(self.state['L1'] != 'Block'): 
                self.x_position += 1
        elif(self.direction == 'W'):
            self.direction = 'S'
            if(self.state['L1'] != 'Block'): 
                self.y_position += 1

    def move_right(self):
        if(self.direction == 'N'):
            self.direction = 'E'
            if(self.state['R1'] != 'Block'): 
                self.x_position += 1
        elif(self.direction == 'E'):
            self.direction = 'S'
            if(self.state['R1'] != 'Block'): 
                self.y_position += 1
        elif(self.direction == 'S'):
            self.direction = 'W'
            if(self.state['R1'] != 'Block'): 
                self.x_position -= 1
        elif(self.direction == 'W'):
            self.direction = 'N'
            if(self.state['R1'] != 'Block'): 
                self.y_position -= 1

    def die(self):
        # Genes list is defined in the coevolution file:
        self.dead = True

class Prey(Species):
    def __init__(self, genes, position, direction):
        super().__init__(genes, position, direction)     
        self.food_energy = 400
            
    def stay_still(self):
        self.energy -= 0.2

    def take_action(self, food_list):
        if(self.state_action_dict[self.state_string] == 0):
            self.move_forward(food_list)
        elif(self.state_action_dict[self.state_string] == 1):
            self.move_left(food_list)
        elif(self.state_action_dict[self.state_string] == 2):
            self.move_right(food_list)
        # Actions randomly select from 2-3 possibilities, this helps to prevent getting stuck in loops:
        elif(self.state_action_dict[self.state_string] == 3):
            if(random.random() < 0.5):
                self.move_forward(food_list)
            else:
                self.move_left(food_list)
        elif(self.state_action_dict[self.state_string] == 4):
            if(random.random() < 0.5):
                self.move_left(food_list)
            else:
                self.move_right(food_list)
        elif(self.state_action_dict[self.state_string] == 5):
            if(random.random() < 0.5):
                self.move_forward(food_list)
            else:
                self.move_right(food_list)
        elif(self.state_action_dict[self.state_string] == 6):
            if(random.random() < 0.5):
                self.move_forward(food_list)
            else:
                self.stay_still()
        elif(self.state_action_dict[self.state_string] == 7):
            if(random.random() < 0.5):
                self.move_left(food_list)
            else:
                self.stay_still()
        elif(self.state_action_dict[self.state_string] == 8):
            if(random.random() < 0.5):
                self.move_right(food_list)
            else:
                self.stay_still()
        elif(self.state_action_dict[self.state_string] == 9):
            if(random.random() < float(1/3)):
                self.move_right(food_list)
            elif(random.random() < float(2/3)):
                self.move_left(food_list)
            else:
                self.stay_still()

        self.fitness += 1
        self.age += 1

    def move_forward(self, food_list):
        super().move_forward()
        self.energy -= 0.2
        if(self.state['F1'] == 'Predator'):
            self.die()
        elif(self.state['F1'] == 'Food'):
            self.energy += self.food_energy
            self.fitness += self.age
            food_index = 0
            for food_x, food_y, eaten in food_list:
                if(food_x == self.x_position and food_y == self.y_position):
                    food_list[food_index] = (-1, -1, True)
                food_index += 1
    
    def move_left(self, food_list):
        super().move_left()
        self.energy -= 0.2
        if(self.state['L1'] == 'Predator'):
            self.die()
        elif(self.state['L1'] == 'Food'):
            self.energy += self.food_energy
            self.fitness += self.age
            food_index = 0
            for food_x, food_y, eaten in food_list:
                if(food_x == self.x_position and food_y == self.y_position):
                    food_list[food_index] = (-1, -1, True)
                food_index += 1
        
    
    def move_right(self, food_list):
        super().move_right()
        self.energy -= 0.2
        if(self.state['R1'] == 'Predator'):
            self.die()
        elif(self.state['R1'] == 'Food'):
            self.energy += self.food_energy
            self.fitness += self.age
            food_index = 0
            for food_x, food_y, eaten in food_list:
                if(food_x == self.x_position and food_y == self.y_position):
                    food_list[food_index] = (-1, -1, True)
                food_index += 1
    
    def update_state(self, world):
        if(self.direction == 'N'):
            self.state['F1'] = world[self.x_position][self.y_position-1]
            self.state['L1'] = world[self.x_position-1][self.y_position]
            try:
                self.state['L2'] = world[self.x_position-2][self.y_position]
            except IndexError:
                self.state['L2'] = 'Empty'
            self.state['R1'] = world[self.x_position+1][self.y_position]
            try:
                self.state['R2'] = world[self.x_position+2][self.y_position]
            except IndexError:
                self.state['R2'] = 'Empty'
        elif(self.direction == 'E'):
            self.state['F1'] = world[self.x_position+1][self.y_position]
            self.state['L1'] = world[self.x_position][self.y_position-1]
            try:
                self.state['L2'] = world[self.x_position][self.y_position-2]
            except IndexError:
                self.state['L2'] = 'Empty'   
            self.state['R1'] = world[self.x_position][self.y_position+1]
            try:
                self.state['R2'] = world[self.x_position][self.y_position+2]
            except IndexError:
                self.state['R2'] = 'Empty'
        elif(self.direction == 'S'):
            self.state['F1'] = world[self.x_position][self.y_position+1]
            self.state['L1'] = world[self.x_position+1][self.y_position]
            try:
                self.state['L2'] = world[self.x_position+2][self.y_position]
            except IndexError:
                self.state['L2'] = 'Empty'
            self.state['R1'] = world[self.x_position-1][self.y_position]
            try:
                self.state['R2'] = world[self.x_position-2][self.y_position]
            except IndexError:
                self.state['R2'] = 'Empty'
        elif(self.direction == 'W'):
            self.state['F1'] = world[self.x_position-1][self.y_position]
            self.state['L1'] = world[self.x_position][self.y_position+1]
            try:
                self.state['L2'] = world[self.x_position][self.y_position+2]
            except IndexError:
                self.state['L2'] = 'Empty'
            self.state['R1'] = world[self.x_position][self.y_position-1]
            try:
                self.state['R2'] = world[self.x_position][self.y_position-2]
            except IndexError:
                self.state['R2'] = 'Empty'
        self.build_state_string()
        if(self.energy <= 0):
            self.die()
     

class Predator(Species):
    def __init__(self, genes, position, direction):
        super().__init__(genes, position, direction)
        self.prey_energy = 500
    
    def stay_still(self):
        self.energy -= 0.1

    def take_action(self, prey_list):
        if(self.state_action_dict[self.state_string] == 0):
            self.move_forward(prey_list)
        elif(self.state_action_dict[self.state_string] == 1):
            self.move_left(prey_list)
        elif(self.state_action_dict[self.state_string] == 2):
            self.move_right(prey_list)
                # Actions randomly selects from 2-3 possibilities, this helps to prevent getting stuck in loops:
        elif(self.state_action_dict[self.state_string] == 3):
            if(random.random() < 0.5):
                self.move_forward(prey_list)
            else:
                self.move_left(prey_list)
        elif(self.state_action_dict[self.state_string] == 4):
            if(random.random() < 0.5):
                self.move_left(prey_list)
            else:
                self.move_right(prey_list)
        elif(self.state_action_dict[self.state_string] == 5):
            if(random.random() < 0.5):
                self.move_forward(prey_list)
            else:
                self.move_right(prey_list)
        elif(self.state_action_dict[self.state_string] == 6):
            if(random.random() < 0.5):
                self.move_forward(prey_list)
            else:
                self.stay_still()
        elif(self.state_action_dict[self.state_string] == 7):
            if(random.random() < 0.5):
                self.move_left(prey_list)
            else:
                self.stay_still()
        elif(self.state_action_dict[self.state_string] == 8):
            if(random.random() < 0.5):
                self.move_right(prey_list)
            else:
                self.stay_still()
        elif(self.state_action_dict[self.state_string] == 9):
            if(random.random() < float(1/3)):
                self.move_right(prey_list)
            elif(random.random() < float(2/3)):
                self.move_left(prey_list)
            else:
                self.stay_still()

        self.age += 1

    def move_forward(self, prey_list):
        super().move_forward()
        self.energy -= 0.7
        if(self.state['F1'] == 'Prey'):
            self.energy += self.prey_energy
            self.fitness += self.age
            prey_index = 0
            for prey in prey_list:
                if(prey.x_position == self.x_position and prey.y_position == self.y_position):
                    prey_list[prey_index].dead = True
                prey_index += 1
    
    def move_left(self, prey_list):
        super().move_left()
        self.energy -= 0.7
        if(self.state['L1'] == 'Prey'):
            self.energy += self.prey_energy
            self.fitness += self.age
            prey_index = 0
            for prey in prey_list:
                if(prey.x_position == self.x_position and prey.y_position == self.y_position):
                    prey_list[prey_index].dead = True
                prey_index += 1
        
    def move_right(self, prey_list):
        super().move_right()
        self.energy -= 0.7
        if(self.state['R1'] == 'Prey'):
            self.energy += self.prey_energy
            self.fitness += self.age
            prey_index = 0
            for prey in prey_list:
                if(prey.x_position == self.x_position and prey.y_position == self.y_position):
                    prey_list[prey_index].dead = True
                prey_index += 1

    def update_state(self, world):
        if(self.direction == 'N'):
            self.state['F1'] = world[self.x_position][self.y_position-1]
            self.state['L1'] = world[self.x_position-1][self.y_position]
            try:
                self.state['F2'] = world[self.x_position][self.y_position-2]
            except IndexError:
                self.state['F2'] = 'Empty'
            self.state['R1'] = world[self.x_position+1][self.y_position]
            try:
                self.state['F3'] = world[self.x_position][self.y_position-3]
            except IndexError:
                self.state['F3'] = 'Empty'
        elif(self.direction == 'E'):
            self.state['F1'] = world[self.x_position+1][self.y_position]
            self.state['L1'] = world[self.x_position][self.y_position-1]
            try:
                self.state['F2'] = world[self.x_position+2][self.y_position]
            except IndexError:
                self.state['F2'] = 'Empty'   
            self.state['R1'] = world[self.x_position][self.y_position+1]
            try:
                self.state['F3'] = world[self.x_position+3][self.y_position]
            except IndexError:
                self.state['F3'] = 'Empty'
        elif(self.direction == 'S'):
            self.state['F1'] = world[self.x_position][self.y_position+1]
            self.state['L1'] = world[self.x_position+1][self.y_position]
            try:
                self.state['F2'] = world[self.x_position][self.y_position+2]
            except IndexError:
                self.state['F2'] = 'Empty'
            self.state['R1'] = world[self.x_position-1][self.y_position]
            try:
                self.state['F3'] = world[self.x_position][self.y_position+3]
            except IndexError:
                self.state['F3'] = 'Empty'
        elif(self.direction == 'W'):
            self.state['F1'] = world[self.x_position-1][self.y_position]
            self.state['L1'] = world[self.x_position][self.y_position+1]
            try:
                self.state['F2'] = world[self.x_position-2][self.y_position]
            except IndexError:
                self.state['F2'] = 'Empty'
            self.state['R1'] = world[self.x_position][self.y_position-1]
            try:
                self.state['F3'] = world[self.x_position-3][self.y_position]
            except IndexError:
                self.state['F3'] = 'Empty'
        self.build_state_string()
        if(self.energy <= 0):
            self.die()