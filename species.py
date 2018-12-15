import itertools
from collections import OrderedDict

class Species:
    def __init__(self, genes, position, direction):
        self.x_position, self.y_position = position
        self.state = {}
        self.direction = direction
        self.energy = 20
        self.age = 0
        self.state_action_dict = {} # This is a dictionary from every possible state to the action that should be taken in this state.
        self.genes = genes
        self.state_string = ''

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
        self.energy -= 0.1
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
        self.energy -= 0.1
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
        self.energy -= 0.1
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

    def stay_still(self):
        pass
    
class Prey(Species):
    def __init__(self, genes, position, direction):
        super().__init__(genes, position, direction)         
        
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
                self.state['L2'] = world[self.x_position-2][self.y_position+2]
            except IndexError:
                self.state['L2'] = 'Empty'
            self.state['R1'] = world[self.x_position+1][self.y_position-1]
            try:
                self.state['R2'] = world[self.x_position+2][self.y_position-2]
            except IndexError:
                self.state['R2'] = 'Empty'
        self.build_state_string()
     
    def take_action(self):
        if(self.state_action_dict[self.state_string] == 0):
            self.move_forward()
        elif(self.state_action_dict[self.state_string] == 1):
            self.move_left()
        elif(self.state_action_dict[self.state_string] == 2):
            self.move_right()

class Predator(Species):
    def __init__(self, genes, position, direction):
        super().__init__(genes, position, direction)
     