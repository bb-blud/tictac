import random as ran

class Player(object):
    mark = None
    
    def __init__(self, mark, game_state):
        self.game_state = game_state
        self.mark = mark
        self.is_winner = False
        
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
    players = (None, None)
    current_player = None
    def __init__(self, size=3):
        # Game size
        self.size = abs(size)

        # Initialize state variables
        self.game_finished = False
        self.step = 1
        self.lines = {'Vertical': {}, 'Horizontal': {}, 'Diagonal': {} }
        self.game_sequence = []

        # For global coordinate transform
        self.transform = lambda (x,y): (x,y)

    def setPlayers(self, player1, player2):
        self.players = player1, player2
        self.current_player = self.players[0]
        
    def setQMap(self, Q):
        self.Q = Q

    def getQMap(self):
        return self.Q
    
    def validMove(self, index):
        if index not in ( m[0] for m in self.game_sequence):
            return True
        return False
            
    def updateState(self, move):
        index , mark = move        
        if self.step == 1:
            self.setTransform(index)
  
        print self.current_player.mark, index
        
        if self.validMove(index):
            self.game_sequence.append( (index, mark) )
            self.Q.updateQ( (self.step,)+tuple( (self.transformIndex(move[0]), move[1]) for move in self.game_sequence) )
        else:
            print "invalid", mark, index
            self.game_finished = True
            return
        
        # Update roster of viable consecutive marks in line
        self.updateLines(self.game_sequence)
        
        # Update game finish state
        self.game_finished = self.updateFinished()

        # Set player to have next turn
        self.current_player = self.players[self.step%2]
        
        # Update step count
        self.step += 1
        
    def takeStep(self):
        move = self.current_player.makeMove()
        self.updateState(move)
            
    def updateFinished(self):
        size = self.size

        # Find 'size' number of consecutive marks in a line, current_player wins
        for direction in ['Vertical', 'Horizontal', 'Diagonal']:
            for line in (self.lines[direction].get(coordinate) for coordinate in range(size) + range(0, size**2 -size , size) ):
                if line is not None and len(line) == size:
                    self.current_player.is_winner = True
                    return True
            
        # All positions filled no winner
        if len(self.game_sequence) >= self.size**2:
            return True
        
        return False        
        
    def resetGame(self):
        self.game_finished = False
        self.step = 1
        self.lines = {'Vertical': {}, 'Horizontal': {}, 'Diagonal': {} }
        self.game_sequence = []
        self.transform = lambda (x,y): (x,y)
        self.current_player = self.players[0]


    def setTransform(self, first_move):
        def compose(f,g):
            return lambda x: f(g(x))
        
        x , y = self.getCoordinates(first_move)
        size = self.size
        
        parity = size+1
        midline = size/2 - 0.5*(parity%2)

        if x > midline:
            reflectX = lambda (x,y): (int(midline - (x - midline)), y)
            self.transform = compose(reflectX, self.transform)
        if y > midline:
            reflectY = lambda (x,y): (x, int(midline - (y - midline)) )
            self.transform = compose(reflectY, self.transform)
        if y > x:
            reflectDiagonal = lambda (x,y): (y,x)
            self.transform = compose(reflectDiagonal, self.transform)

    def getCoordinates(self, index):
        x , y = index%self.size, index//self.size
        return x,y
    
    def getIndex(self, (x,y)):
        index = x + y*self.size
        return index
    
    def transformIndex(self, index):
        return self.getIndex(self.transform(self.getCoordinates(index)))
    
    def updateLines(self, sequence):
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
    
                    



        # if self.step % 2 == 1:
        #     move = self.players[0].makeMove()
        #     self.game_sequence.append(move)
        #     self.Q.updateQ( (self.step,)+tuple(move for move in self.game_sequence) )
        # else:
        #     move = self.players[1].makeMove()
        #     self.game_sequence.append(move)
        #     self.Q.updateQ( (self.step,)+tuple(move for move in self.game_sequence) )
        

                    
    ################ Tests ####################

    def makeGrid(self,sequence):
        size = self.size
        grid = [ [' ' for i in range(size)] for j in range(size) ]
        
        for p in sequence:
            x, y = self.getCoordinates(p[0])
            grid[y][x] = p[1]
            
        return grid
    
    def printGrid(self, grid):
        for row in grid:
            print row

    # def testTransform(self):
        
    #     tests = [
    #         [3, 2, (2, 'O')],  #  
    #         [3, 8, (8, 'O')],  # All corners are equivalent
    #         [3, 6, (6, 'O')],  #

    #         [5, 12, (12, 'X')], # Center point doesn't move
            
    #         [4, 10, (10,'1'),(2,'2'),(3,'3'),(7,'4'),(11,'5')]] # Order is preserved

    #     for i, test in enumerate(tests):
    #         self.resetGame()
            
    #         print "Test: ", i
    #         self.size = test[0]
    #         start = test[1]
    #         self.setTransform(start)

    #         point = self.getCoordinates(start)
    #         print "point: {}, Index: {}".format(point, start)
    #         print "tpoint: {}, Index: {}".format(self.transform(point), self.getIndex(self.transform(point)) )
    #         print

    #         seq = test[2:]
    #         print seq
    #         for row in self.makeGrid(seq):
    #             print row
    #         print

    #         tseq = [(self.getIndex(self.transform(self.getCoordinates(s[0]))), s[1]) for s in seq]
    #         print tseq
    #         for row in self.makeGrid(tseq):
    #             print row
    #         print

    #         ttseq = [(self.getIndex(self.transform(self.getCoordinates(s[0]))), s[1]) for s in tseq]
    #         print ttseq
    #         for row in self.makeGrid(ttseq):
    #             print row
    #         print 'END Test: ', i

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
