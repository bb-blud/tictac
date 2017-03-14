"""
This module houses the Player, QMap and GameState classes. All information
about the state of a game is stored and modified here.

"""

class GameState(object):
    """
    Contains the entire state of the game, cosisting of a sequence of moves,
    two players, and an instance of QMap to be used by the player agents.

    """
    players = (None, None)
    current_player = None
    def __init__(self, size=3, learning=False):        
        # Global QMap
        self.QM = QMap()
        
        # Game size
        self.size = abs(size)
        
        # Initialize state variables
        self.learning = learning
        self.game_finished = False
        self.step = 1
        self.lines = {'Vertical':   {},  #Dictionary of dictionaries houses all lines
                      'Horizontal': {},  #in the current game. Lines are referenced by
                      'D-pos':      {},  #the coordinate common to all of its members,
                      'D-neg':      {} } #except diagonals since there is only one of each
        self.game_sequence = []

        # For global coordinate transform
        self.transform = lambda (x,y): (x,y)
        self.inverseTF = lambda (x,y): (x,y)

    def setPlayers(self, player1, player2):
        self.players = player1, player2
        self.current_player = self.players[0]
        
    def otherPlayer(self):
        return [p for p in self.players if p is not self.current_player][0]
        
    def setQMap(self, QM):
        self.QM = QM
    
    def validMove(self, index, sequence):
        if index not in ( m[0] for m in sequence):
            return True
        return False
    
    def takeStep(self):
        move = self.current_player.makeMove()
        self.updateState(move)

    def updateState(self, move):
        index , mark = move        
        if self.step == 1:
            self.setTransform(index)

        if self.validMove(index, self.game_sequence):
             self.game_sequence.append( (index, mark) )
             if self.learning:
                 self.QM.visitQ(tuple( (self.transformIndex(index), mark) for index, mark in self.game_sequence) )
        else:
            print "<----------------------invalid move by {} at index {}----------------------------->".format( mark, index)
            self.game_finished = True
            return
        
        # Update roster of viable consecutive marks in line
        self.lines = self.findLines(self.game_sequence)
        
        # Update game finish state
        self.game_finished = self.updateFinished()

        # Update Q map
        if self.game_finished and self.learning:
            t_game_sequence = [ (self.transformIndex(index) , mark ) for index, mark in self.game_sequence ]
            
            r = { (True , False) :  1.0,
                  (False, False) :  0.0,
                  (False, True ) : -1.0 }[self.players[0].is_winner, self.players[1].is_winner]
            
            self.QM.updateQ(t_game_sequence, r)
            
        # Set player to have next turn
        self.current_player = self.otherPlayer()
        
        # Update step count
        self.step += 1
        
    def updateFinished(self):
        size = self.size

        lv = len(self.lines['Vertical'].keys())
        lh = len(self.lines['Horizontal'].keys())
        
        # Find 'size' number of consecutive marks in a line, current_player wins
        for direction in ['Vertical', 'Horizontal', 'D-pos', 'D-neg']:
                        
            keys = range(size)   # The possible line keys range from 0 to size -1, unless line is diagonal
            if direction in ['D-pos', 'D-neg']:
                keys = [0]
                
            for line in (self.lines[direction].get(coordinate) for coordinate in keys ):
                if line is not None and len(line) - 1 == size: # line's first entry is players mark
                    self.current_player.is_winner = True
                    return True

        # If there are no lines left that can have size amount of marks no player wins
        if lv == size and lh == size and self.lines['D-pos'].get(0, None) == None and self.lines['D-neg'].get(0, None) == None:
            Nones = [None for _ in range(size)]
            if [self.lines['Vertical'][k] for k in range(size) ] == Nones and [self.lines['Horizontal'][k] for k in range(size) ] == Nones:
                return True
        
        return False        

    def isTie(self, sequence):
        size = self.size
        lines = self.findLines(sequence)

        lv = len(lines['Vertical'].keys())   #How many Vertical lines have been explored up to this point
        lh = len(lines['Horizontal'].keys()) #How many Horizontal lines have been explored up to this point

        #First remember that if both players place marks on a line it becomes None or "not viable"
        #So if all horizontals and all verticals have been played upon, and both diagonals are None (there is code repetition see updateFinished)
        if lv == size and lh == size and lines['D-pos'].get(0, None) == None and lines['D-neg'].get(0, None) == None:            
            Nones = [None for _ in range(size)]
            # If further, all vericals have and horizontals are None, then there are no viable lines to try to win its a tie
            if [lines['Vertical'][k] for k in range(size) ] == Nones and [lines['Horizontal'][k] for k in range(size) ] == Nones:
                return True
                
        return False
        
    def resetGame(self):
        self.game_finished = False
        self.step = 1
        self.lines = {'Vertical': {}, 'Horizontal': {}, 'D-pos': {}, 'D-neg': {} }
        self.game_sequence = []
        self.transform = lambda (x,y): (x,y)
        self.inverseTF = lambda (x,y): (x,y)
        self.current_player = self.players[0]
        for p in self.players:
            if p:
                p.is_winner = False

    def setTransform(self, first_move):        
        """ 
        Build coordinate transform from reflections about the board's vertical, 
        horizontal and d-pos lines of symmetry, gradually as needed  
        
        """
        #Helper function composes two functions
        def compose(f,g):
            return lambda x: f(g(x))
        
        x , y = self.getCoordinates(first_move)
        size = self.size
        
        parity = size+1                    # For even numbered boards, vertical and horizontal
        midline = size/2 - 0.5*(parity%2)  # lines of symmetry are halfway between integer values
        
        transformations = []
        if x > midline:  # If position lies below horizontal
            reflectX = lambda (x,y): (int(midline - (x - midline)), y)
            x , y = reflectX( (x,y) )
            transformations.append(reflectX)
                
            
        if y > midline:  # If position lies to the right of vertical
            reflectY = lambda (x,y): (x, int(midline - (y - midline)) )
            x , y = reflectY( (x,y) )
            transformations.append(reflectY)
                
        if y > x:        # If position lies below main 'positive' diagonal
            reflectDiagonal = lambda (x,y): (y,x)
            transformations.append(reflectDiagonal)
                
        for k, trans in enumerate(transformations):
            self.transform = compose(trans, self.transform)
            self.inverseTF = compose(transformations[-(k+1) ], self.inverseTF)

    def getCoordinates(self, index):
        x , y = index%self.size, index//self.size  #Remainder mod n of an index gives the x coordinate,
        return x,y                                 #Number of times n goes in index gives the y coordinate

    def getIndex(self, (x,y)):
        index = x + y*self.size
        return index
   
    def transformIndex(self, index):
        return self.getIndex(self.transform(self.getCoordinates(index)))
    
    def inverseTFIndex(self, index):
        return self.getIndex(self.inverseTF(self.getCoordinates(index)))
    

    def findLines(self, sequence):
        """ 
        This method is a workhorse for most of the game measuring logic, it finds
        all lines in the current state of the game 

        """      
        size = self.size
        lines_in_seq = {'Vertical': {}, 'Horizontal': {}, 'D-pos': {}, 'D-neg': {} }

        ###############
        # Evaluate and append a line in a particular direction at a particular coordinate      
        def tallyLine(direction, coordinate, move):
            tic = 0
            tac = move[1]
            current_line = lines_in_seq[direction].get(coordinate, 'Empty')

            if current_line is not None and current_line is 'Empty':
                lines_in_seq[direction][coordinate] = [tac, move[0]]

            elif current_line is not None and current_line[tic] == tac:
                lines_in_seq[direction][coordinate].append(move[0]) if move[0] not in lines_in_seq[direction][coordinate] else None

            else:
                lines_in_seq[direction][coordinate] = None
                
        ###############
        # Check if each point in the game sequence belongs to a line or not
        for move in sequence:
            x , y = self.getCoordinates(move[0])

            # Tally of horizontal and vertical lines
            for direction in ['Horizontal', 'Vertical']:
                coordinate = {'Vertical': x, 'Horizontal': y}[direction]
                tallyLine(direction, coordinate, move)
                    
            # Tally of the two possible diagonal lines
            if x == y:   
                tallyLine('D-pos', 0, move)
            if x + y == size - 1:
                tallyLine('D-neg', 0, move)

        return lines_in_seq

    def belongsToLine(self, index, direction, line):
        """ 
        Checks if a particular index belongs to a line 

        """        
        first_point = 1  
        if direction == 'Horizontal': # Check if index's y coordinate is the same as line's first point
            if self.getCoordinates(index)[1] == self.getCoordinates(line[first_point])[1]:
                return True
        elif direction == 'Vertical': # Check if index's x coordinate is the same as line's first point
            if self.getCoordinates(index)[0] == self.getCoordinates(line[first_point])[0]:
                return True
        else:
            x, y = self.getCoordinates(index)

            if direction == 'D-pos' and  x == y:  # points in positive diagonal have equal x and y coordinates
                return True
            if direction == 'D-neg' and  x + y == self.size - 1: # some of coordinates negative diagonal point is n -1
                return True
            return False

    def indexToWin(self, direction, line):
        """
        In a line of length size-1 return the index that fills
        it into a winning line of length size 

        """       
        size = self.size
        if len(line[1:]) != size - 1:
            return None

        ## Experiment in avoiding conditional if then statements
        i = 0
        if direction in ['Vertical' , 'Horizontal']:
            # A vertical line is defined by the x coordinate of its points
            # A horizontal line is defined byt the y coordinate of its points
            i = {'Vertical': line[1]%size, 'Horizontal' : line[1]//size }[direction]

        return  {'D-neg'     : [k for k in range(size -1, size**2, size-1)[:-1] if k not in line[1:]][0],
                 
                 'D-pos'     : [k for k in range(0, size**2, size+1) if k not in line[1:]][0],
                 
                 'Vertical'  : [k for k in range(i, i + size**2, size) if k not in line[1:]][0],
                 
                 'Horizontal': [k for k in range(i*size, i*size +size) if k not in line[:1]][0]  } [direction]

                 #Explanation of return statement above:
                 #For each line on the grid, the index of its points belong to an arithmetic progression.
                 #For example, the first horizontal line's indices are; 0,1,2..size-1 
                 #Ex 6x6:
                 #  0 1 2 3 4 5
                 #  6 7
                 #  12  14
                 #  18    21
                 #  24      28
                 #  30        35
                 # So for horizontals step size is 1, shift by n to get all others
                 # For verticals step size is n, shift by i to get all others
                 # For positive diagonal step size is n+1
                 # for negative diagonal step size is n-1 


#####################
#   Debugging
#####################
    
    def setGameSequence(self, sequence):
        self.game_sequence = sequence
        self.step += len(sequence)

    def setCurrentPlayer(self, player):
        self.current_player = player
        
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
    
    def printGame(self):
        self.printGrid(self.makeGrid(self.game_sequence))
        print "horizontals: ", self.lines['Horizontal']
        print "verticals: ", self.lines['Vertical']
        print "d-pos: ", self.lines['D-pos']
        print "d-neg: ", self.lines['D-neg']                     
        print
        
    def exploreQ(self,d):
        Q = self.QM.Q
        if Q == {}:
            print Q
        else:
            M = max(len(seq) for seq in Q.keys())
            for k in range(1,M/d):
                print "Explored Moves at step", k
                explored = sorted( [(seq , Q[seq]) for seq in Q if len(seq) == k], key=lambda t:t[1] )

                for seq, val  in explored:
                    print seq, val
                print        
###########################################################
#           Testing functions and code logic
###########################################################

    def testTransform(self):
        
        tests = [
            [3, 2, (2, 'O')],  #  
            [3, 8, (8, 'O')],  # All corners are equivalent
            [3, 6, (6, 'O')],  #

            [5, 12, (12, 'X')], # Center point doesn't move
            
            [4, 10, (10,'1'),(2,'2'),(3,'3'),(7,'4'),(11,'5')],  # Order is preserved

            [3, 3, (3, 'X')],

            [3, 7, (7, 'X')] ]  

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

            tseq = [(self.transformIndex(s[0]), s[1]) for s in seq]
            print tseq
            for row in self.makeGrid(tseq):
                print row
            print

            ttseq = [(self.inverseTFIndex(s[0]), s[1]) for s in tseq]
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
