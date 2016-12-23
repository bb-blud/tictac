import random as ran

class Player(object):
    mark = None
    
    def __init__(self, mark, game_state):
        self.game_state = game_state
        self.mark = mark
        
    def makeMove(self):
        pass

class QMap(object):
   
    def __init__(self):
        self.Q = {}
        
    def updateQ(self, move_sequence):
        if not self.Q.get(move_sequence, False):
            self.Q[move_sequence] = 1
        else:
            self.Q[move_sequence] += 1

    def getQ(self):
        return self.Q
            
class GameState(object):
    player1 = None
    player2 = None

    def __init__(self, size=3):

        # Initialize state variables
        self.winner = False
        self.step = 1
        self.lines = {'Vertical': {}, 'Horizontal': {}, 'Diagonal': {} }
        self.game_sequence = []
        
        # Game size
        self.size = size

    def setPlayers(self, player1, player2):
        self.player1 = player1
        self.player2 = player2

    def setQMap(self, Q):
        self.Q = Q
        
    def getQMap(self):
        return self.Q
    
    def resetGame(self):
        self.winner = False
        self.step = 1
        self.lines = {'Vertical': {}, 'Horizontal': {}, 'Diagonal': {} }
        self.game_sequence = []
    
    def gameFinished(self):
        size = self.size
        # Update roster of consecutive inline marks
        self.findLines(self.game_sequence)

        # Find 'size' number of consecutive marks in a line
        for direction in ['Vertical', 'Horizontal', 'Diagonal']:
            for line in (self.lines[direction].get(coordinate) for coordinate in range(size) + range(0, size**2 -size , size) ):
                if line is not None and len(line) == size:
                    return True
            
        # All positions filled no winner
        if len(self.game_sequence) >= self.size**2:
            return True
        
        return False
        
    def getCoordinates(self, point):
        x , y = point%self.size, point//self.size
        return x,y
    
    def findLines(self, sequence):
        size = self.size
        if sequence == []:
            return
        
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
                orientation = x==y
                if not self.lines['Diagonal'].get(orientation, False):
                    self.lines['Diagonal'][orientation] = [point]
                    
                elif self.lines['Diagonal'][orientation] is not None and self.lines['Diagonal'][orientation][first_point][tic] == tac:
                    self.lines['Diagonal'][orientation].append(point) if point not in self.lines['Diagonal'][orientation] else None
                    
                else:
                    self.lines['Diagonal'][orientation] = None
    
                    
    def takeStep(self):
        if self.step % 2 == 1:
            move = self.player1.makeMove()
            self.game_sequence.append(move)
            self.Q.updateQ( (self.step,)+tuple(move for move in self.game_sequence) )
        else:
            move = self.player2.makeMove()
            self.game_sequence.append(move)
            self.Q.updateQ( (self.step,)+tuple(move for move in self.game_sequence) )
            
        # for row in self.makeGrid(self.game_sequence):
        #     print row
        # print 
        self.step += 1
                    
    ################ Tests ####################

    def makeGrid(self,sequence):
        size = self.size
        grid = [ [' ' for i in range(size)] for j in range(size) ]
        
        for p in sequence:
            x, y = p[0]%size, p[0]//size
            grid[y][x] = p[1]
            
        return grid
        

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
        

    #     for t, test in enumerate(tests):
            
    #         # Grid            
    #         grid = self.makeGrid(test)

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
