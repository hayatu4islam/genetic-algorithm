class Species:
    def __init__(self, position, direction):
        self.pos_x, self.pos_y = position
        self.direction = direction
        self.energy = 20
        self.age = 0

    def move_forward(self):
        self.energy -= 0.1
        if(self.state['F1'] != 'Block'):
            if(self.direction == 'N'):
                self.pos_y -= 1
            elif(self.direction == 'E'):
                self.pos_x += 1
            elif(self.direction == 'S'):
                self.pos_y += 1
            elif(self.direction == 'W'):
                self.pos_x -= 1
        
    def move_left(self):
        self.energy -= 0.1
        if(self.state['L1'] != 'Block'): 
            if(self.direction == 'N'):
                self.direction = 'W'
                self.pos_x -= 1
            elif(self.direction == 'E'):
                self.direction = 'N'
                self.pos_y -= 1
            elif(self.direction == 'S'):
                self.direction = 'E'
                self.pos_x += 1
            elif(self.direction == 'W'):
                self.direction = 'S'
                self.pos_y += 1

    def move_right(self):
        pass
    
    def move_back(self):
        pass
    
    def stay_still(self):
        pass
    
class Prey(Species):
    def __init__(self):
        super.__init__(self)
    
    def get_state(self, world):
        if(self.direction == 'N'):
            self.state['F1'] = world[self.pos_x][self.pos_y-1]
            self.state['L1'] = world[self.pos_x-1][self.pos_y]
            try:
                self.state['L2'] = world[self.pos_x-2][self.pos_y]
            except IndexError:
                self.state['L2'] = 'Empty'
            self.state['R1'] = world[self.pos_x+1][self.pos_y]
            try:
                self.state['R2'] = world[self.pos_x+2][self.pos_y]
            except IndexError:
                self.state['R2'] = 'Empty'
        elif(self.direction == 'E'):
            self.state['F1'] = world[self.pos_x+1][self.pos_y]
            self.state['L1'] = world[self.pos_x][self.pos_y-1]
            try:
                self.state['L2'] = world[self.pos_x][self.pos_y-2]
            except IndexError:
                self.state['L2'] = 'Empty'   
            self.state['R1'] = world[self.pos_x][self.pos_y+1]
            try:
                self.state['R2'] = world[self.pos_x][self.pos_y+2]
            except IndexError:
                self.state['R2'] = 'Empty'
        elif(self.direction == 'S'):
            self.state['F1'] = world[self.pos_x][self.pos_y+1]
            self.state['L1'] = world[self.pos_x+1][self.pos_y]
            try:
                self.state['L2'] = world[self.pos_x+2][self.pos_y]
            except IndexError:
                self.state['L2'] = 'Empty'
            self.state['R1'] = world[self.pos_x-1][self.pos_y]
            try:
                self.state['R2'] = world[self.pos_x-2][self.pos_y]
            except IndexError:
                self.state['R2'] = 'Empty'
        elif(self.direction == 'W'):
            self.state['F1'] = world[self.pos_x-1][self.pos_y]
            self.state['L1'] = world[self.pos_x][self.pos_y+1]
            try:
                self.state['L2'] = world[self.pos_x-2][self.pos_y+2]
            except IndexError:
                self.state['L2'] = 'Empty'
            self.state['R1'] = world[self.pos_x+1][self.pos_y-1]
            try:
                self.state['R2'] = world[self.pos_x+2][self.pos_y-2]
            except IndexError:
                self.state['R2'] = 'Empty'
    