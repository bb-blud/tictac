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

    def visitQ(self, sequence):
        if not self.Q.get(sequence, False):
            self.Q[sequence] = 0

    def updateQ(self, game, players, size):
        
        if True not in (player.is_winner for player in players):
            reward = 0
        else:
            reward = size**4 / len(game)
            winner = [p for p in players if p.is_winner][0]
            sgn = { players[0].mark : 1, players[1].mark : -1 }[winner.mark]
            
            for i in range(1, len(game) - 1):
                sub_sequence = tuple(game[:i])
                self.Q[sub_sequence] += sgn * reward
            self.Q[tuple(game)] = sgn * reward * size**4

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
        self.lines = {'Vertical': {}, 'Horizontal': {}, 'D-pos': {}, 'D-neg':{} }
        self.game_sequence = []

        # For global coordinate transform
        self.transform = lambda (x,y): (x,y)

    def setPlayers(self, player1, player2):
        self.players = player1, player2
        self.current_player = self.players[0]
        
    def setQMap(self, Q):
        self.QMap = Q

    def getQMap(self):
        return self.QMap
    
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
             self.QMap.visitQ(tuple( (self.transformIndex(index), mark) for index, mark in self.game_sequence) )
        else:
            print "<----------------------invalid move by {} at index {}----------------------------->".format( mark, index)
            self.game_finished = True
            return
        
        # Update roster of viable consecutive marks in line
        self.lines = self.findLines(self.game_sequence)
        
        # Update game finish state
        self.game_finished = self.updateFinished()

        # Update Q map
        if self.game_finished:
            t_game_sequence = [ (self.transformIndex(index) , mark ) for index, mark in self.game_sequence ]
            self.QMap.updateQ(t_game_sequence, self.players, self.size)
        #     for key in self.Q.getQ().keys():
        #         print key
            
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
                        
            keys = range(size)    # The possible line keys range from 0 to size -1, unless line is diagonal
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

        lv = len(lines['Vertical'].keys())
        lh = len(lines['Horizontal'].keys())
        
        if lv == size and lh == size and lines['D-pos'].get(0, None) == None and lines['D-neg'].get(0, None) == None:
            Nones = [None for _ in range(size)]
            if [lines['Vertical'][k] for k in range(size) ] == Nones and [lines['Horizontal'][k] for k in range(size) ] == Nones:
                return True
                
        return False
        
    def resetGame(self):
        self.game_finished = False
        self.step = 1
        self.lines = {'Vertical': {}, 'Horizontal': {}, 'D-pos': {}, 'D-neg': {} }
        self.game_sequence = []
        self.transform = lambda (x,y): (x,y)
        self.current_player = self.players[0]
        for p in self.players:
            if p:
                p.is_winner = False

    def setTransform(self, first_move):
        def compose(f,g):
            return lambda x: f(g(x))
        
        x , y = self.getCoordinates(first_move)
        size = self.size
        
        parity = size+1
        midline = size/2 - 0.5*(parity%2)

        if x > midline:
            reflectX = lambda (x,y): (int(midline - (x - midline)), y)
            x , y = reflectX( (x,y) )
            self.transform = compose(reflectX, self.transform)
            
            
        if y > midline:
            reflectY = lambda (x,y): (x, int(midline - (y - midline)) )
            x , y = reflectY( (x,y) )
            self.transform = compose(reflectY, self.transform)
            
        if y > x:
            reflectDiagonal = lambda (x,y): (y,x)
            self.transform = compose(reflectDiagonal, self.transform)


    def otherPlayer(self):
        return [p for p in self.players if p is not self.current_player][0]

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
        lines_in_seq = {'Vertical': {}, 'Horizontal': {}, 'D-pos': {}, 'D-neg': {} }

        ###############
        # Evaluate and append a line in a particular direction at a particular coordinate      
        def tallyLine(direction, coordinate, move):
            tic = 0
            tac = move[1]
            current_line = lines_in_seq[direction].get(coordinate, 'Empty')

            if current_line is not None and current_line is 'Empty':
                lines_in_seq[direction][coordinate] = [tac, move[0]]

            elif current_line is not None and current_line[tic]== tac:
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
        first_point = 1
        if direction == 'Horizontal':
            if self.getCoordinates(index)[1] == self.getCoordinates(line[first_point])[1]:
                return True
        elif direction == 'Vertical':
            if self.getCoordinates(index)[0] == self.getCoordinates(line[first_point])[0]:
                return True
        else:
            x, y = self.getCoordinates(index)
            u, v = self.getCoordinates(line[first_point])
            slope = (1.*v - y)/(u - x)
            if direction == 'D-pos' and slope == 1:
                return True
            if direction == 'D-neg' and slope == -1:
                return True
            return False
            
    def indexToWin(self, direction, line):
        size = self.size
        if len(line[1:]) != size - 1:
            return None
        
        i = {'Vertical': line[1]%size, 'Horizontal' : line[1]//size }[direction]
        
        return  {'D-neg'     : [k for k in range(size -1, size**2, size-1)[:-1] if k not in line[1:]][0],
                 
                 'D-pos'     : [k for k in range(0, size**2, size+1) if k not in line[1:]][0],
                 
                 'Vertical'  : [k for k in range(i, i + size**2, size) if k not in line[1:]][0],
                 
                 'Horizontal': [k for k in range(i*size, i*size +size) if k not in line[:1]][0]  } [direction]

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
