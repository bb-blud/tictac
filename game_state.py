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
  
        #print self.current_player.mark, index # For debugging
        
        if self.validMove(index):
            self.game_sequence.append( (index, mark) )
            self.Q.updateQ( (self.step,)+tuple( (self.transformIndex(move[0]), move[1]) for move in self.game_sequence) )
        else:
            print "invalid move by {} at index {}".format( mark, index)
            self.game_finished = True
            return
        
        # Update roster of viable consecutive marks in line
        self.lines = self.findLines(self.game_sequence)
        
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
            
            keys = range(size)    # The possible line keys range from 0 to size -1, unless line is diagonal
            if direction == 'Diagonal':
                keys = ['pos', 'neg']
                
            for line in (self.lines[direction].get(coordinate) for coordinate in keys ):
                if line is not None and len(line[1:]) == size:
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
    


        
    def findLines(self, sequence):
        size = self.size
        lines_in_seq = {'Vertical': {}, 'Horizontal': {}, 'Diagonal': {} }

        ###############
        # Evaluate and append a line in a particular direction at a particular coordinate      
        def tallyLine(direction, coordinate, point):
            first_point = 1  # Element at index 0 is the player's mark (i.e. X or O)
            tic = 1
            tac = point[1]
            current_line = lines_in_seq[direction].get(coordinate, 'Empty')

            if current_line is not None and current_line is 'Empty':
                lines_in_seq[direction][coordinate] = [tac, point]

            elif current_line is not None and current_line[first_point][tic] == tac:
                lines_in_seq[direction][coordinate].append(point) if point not in lines_in_seq[direction][coordinate] else None

            else:
                lines_in_seq[direction][coordinate] = None
                
        ###############
        # Check if each point in the game sequence belongs to a line or not
        for point in sequence:
            x , y = self.getCoordinates(point[0])

            # Tally of horizontal and vertical lines
            for direction in ['Horizontal', 'Vertical']:
                coordinate = {'Vertical': x, 'Horizontal': y}[direction]
                tallyLine(direction, coordinate, point)
                    
            # Tally of the two possible diagonal lines
            if x == y:
                tallyLine('Diagonal', 'pos', point)
            if x + y == size - 1:
                tallyLine('Diagonal', 'neg', point)

        return lines_in_seq




                    
###########################################################
#           Testing functions and code logic
###########################################################

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

    def testTransform(self):
        
        tests = [
            [3, 2, (2, 'O')],  #  
            [3, 8, (8, 'O')],  # All corners are equivalent
            [3, 6, (6, 'O')],  #

            [5, 12, (12, 'X')], # Center point doesn't move
            
            [4, 10, (10,'1'),(2,'2'),(3,'3'),(7,'4'),(11,'5')]] # Order is preserved

        for i, test in enumerate(tests):
            self.resetGame()
            
            print "Test: ", i
            self.size = test[0]
            start = test[1]
            self.setTransform(start)

            point = self.getCoordinates(start)
            print "point: {}, Index: {}".format(point, start)
            print "tpoint: {}, Index: {}".format(self.transform(point), self.getIndex(self.transform(point)) )
            print

            seq = test[2:]
            print seq
            for row in self.makeGrid(seq):
                print row
            print

            tseq = [(self.getIndex(self.transform(self.getCoordinates(s[0]))), s[1]) for s in seq]
            print tseq
            for row in self.makeGrid(tseq):
                print row
            print

            ttseq = [(self.getIndex(self.transform(self.getCoordinates(s[0]))), s[1]) for s in tseq]
            print ttseq
            for row in self.makeGrid(ttseq):
                print row
            print 'END Test: ', i

    def test_lines(self):
        size = self.size
        # Test cases for lines as a global class variable
        tests = [ 
                  ((size+1,'O'),(size*size -1,'O')),       # Positive Diagonal

                  ((size-1,'X'),(size*size - size, 'X')),  # Negative Diagonal

                  ((0,'X'), (1,'X'),(2,'X'), (4,'X')),     # Several in row

                  ((0,'X'), (10,'X'), (15,'X'), (20,'X')), # Several in column

                  tuple( (u, ran.choice(['X','O']) ) for u in 

                          set([ ran.randint(0,size*size - 1) for _ in range(3*size)]) ) #random sequence of unique moves

                  ]
        

        for t, test in enumerate(tests):
            
            # Grid            
            grid = self.makeGrid(test)

            #####Test#####
            print "Test: ", t, test            
            print
            self.printGrid(grid)
            print

            lines_in_seq = self.findLines(test)
            for direction in lines_in_seq:
                print direction
                print [ (l, lines_in_seq[direction][l]) for l in lines_in_seq[direction] if
                    lines_in_seq[direction][l] is not None and len(lines_in_seq[direction][l]) >1 ]
            self.resetGame()
