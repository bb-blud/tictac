import random as ran

class Player(object):
    mark = None
    def __init__(self, one, game_state):
        self.game_state = game_state
        
        if one:
            self.mark = 'X'
        else:
            self.mark = 'O'
            
class GameState(object):

    def __init__(self, size=3):

        # Initialize state variables
        self.done = False
        self.step = 0
        self.lines = {'Vertical': {}, 'Horizontal': {}, 'Diagonal': {} }
        self.game_sequence = ()
        
        # Game size
        self.size = size


    def getCoordinates(self, point):
        x , y = point%self.size, point//self.size
        return x,y
    
    def findLines(self, sequence):
        size = self.size
        
        for point in sequence:
            first_point = 0
            tic = 1
            tac = point[1]
            x , y = self.getCoordinates(point[0])

            # Tally of horizontal and vertical lines
            for direction in ['Horizontal', 'Vertical']:
                coordinate = {'Vertical': x, 'Horizontal': y}[direction]

                if not self.lines[direction].get(coordinate, False):
                    self.lines[direction][coordinate] = [point]
                    
                elif self.lines[direction][coordinate] is not None and self.lines[direction][coordinate][first_point][tic] == tac:
                    self.lines[direction][coordinate].append(point) if point not in self.lines[direction][coordinate] else None
                    
                else:
                    self.lines[direction][coordinate] = None
                    
            # Tally of the two possible diagonal lines
            if x == y or x + y == size - 1:
                direction = x==y
                if not self.lines['Diagonal'].get(direction, False):
                    self.lines['Diagonal'][direction] = [point]
                    
                elif self.lines['Diagonal'][direction] is not None and self.lines['Diagonal'][direction][first_point][tic] == tac:
                    self.lines['Diagonal'][direction].append(point) if point not in self.lines['Diagonal'][direction] else None
                else:
                    self.lines['Diagonal'][direction] = None

                    
    ################ Tests ####################

    # def test_lines(self, global_dic = True):
    #     size = self.size
    #     if global_dic:
    #         # Test cases for lines as a global class variable
    #         tests = [ 
    #                   ((size+1,'O'),(size*size -1,'O')),       # Positive Diagonal

    #                   ((size-1,'X'),(size*size - size, 'X')),  # Negative Diagonal

    #                   ((0,'X'), (1,'X'),(2,'X'), (4,'X')),     # Several in row

    #                   ((0,'X'), (10,'X'), (15,'X'), (20,'X')), # Several in column

    #                   tuple( (u, ran.choice(['X','O']) ) for u in 

    #                           set([ ran.randint(0,size*size - 1) for _ in range(3*size)]) ) #random sequence of unique moves

    #                   ]
    #     else:
    #     # Test cases for lines as an internally generated and returned variable in method findLines
    #         tests = [ ((0,'X'), (0,'X')),                      # Repeat

    #                   ((size+1,'O'),(size*size -1,'O')),       # Positive Diagonal

    #                   ((size-1,'X'),(size*size - size, 'X')),  # Negative Diagonal

    #                   ((0,'X'), (1,'X'),(2,'X'), (4,'X')),     # Several in row

    #                   ((0,'X'), (10,'X'), (15,'X'), (20,'X')), # Several in column

    #                   ((2, 'X'), (4, 'O'), (5, 'X'), (6, 'X'), (7, 'X'), (9, 'X'), (15, 'X'), (16, 'X'), (19, 'O'), (20, 'X'), (21, 'X'), (23, 'O'), (24, 'X')),

    #                   tuple( (u, ran.choice(['X','O']) ) for u in 

    #                           set([ ran.randint(0,size*size - 1) for _ in range(3*size)]) ) #random sequence of unique moves

    #                   ]
        
    #     # Grid
    #     for t, test in enumerate(tests):
    #         grid = [ [' ' for i in range(size)] for j in range(size) ]
    #         for p in test:
    #             x, y = p[0]%size, p[0]//size
    #             grid[y][x] = p[1]


    #         #####Test#####
    #         print "Test: ", t, test            
    #         print
    #         for row in grid:
    #             print row

    #         print
    #         if global_dic:
    #             self.findLines(test)
    #             for direction in self.lines:
    #                 print direction
    #                 print [
    #                     (l, self.lines[direction][l]) for l in self.lines[direction] \

    #                     if \
                        
    #                        self.lines[direction][l] is not None and len(self.lines[direction][l]) >1
    #                 ]
                
    #         else:
    #             #lines as local variable
    #             lns = self.findLines(test)  
    #             for direction in lns:
    #                 lines = { coord : lns[direction][coord] for coord in lns[direction] if lns[direction][coord] is not None }
    #                 print direction, [(line, lns[direction][line]) for line in lines if len(lns[direction][line]) > 1]
