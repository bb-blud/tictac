import random as ran
class GameState(object):

    def __init__(self, size=3):
        self.size = size
        

    def getCoordinates(self, point):
        x , y = point%self.size, point//self.size
        return x,y
    
    def findLines(self, sequence):
        
        lines = {'Vertical': {}, 'Horizontal': {}, 'Diagonal': {} }
        size = self.size
        
        for point in sequence:
            first_point = 0
            tic = 1
            tac = point[1]
            x , y = self.getCoordinates(point[0])

            # Tally of horizontal and vertical lines
            for direction in ['Horizontal', 'Vertical']:
                coordinate = {'Vertical': x, 'Horizontal': y}[direction]

                if not lines[direction].get(coordinate, False):
                    lines[direction][coordinate] = [point]
                    
                elif lines[direction][coordinate][first_point][tic] == tac and lines[direction][coordinate] is not None:
                    lines[direction][coordinate].append(point)
                    
                else:
                    lines[direction][coordinate] = None
                    
            # Tally of the two possible diagonal lines
            if x == y or x + y == size - 1:
                direction = x==y
                if not lines['Diagonal'].get(direction, False):
                    lines['Diagonal'][direction] = [point]
                    
                elif lines['Diagonal'][direction][first_point][tic] == tac and lines['Diagonal'][direction] is not None:
                    lines['Diagonal'][direction].append(point)
                else:
                    lines['Diagonal'][direction] = None
            
        return lines   

    
    
    ################ Tests ####################

    def test_lines(self):
        size = self.size
        # TODO: ((2, 'X'), (4, 'O'), (5, 'X'), (6, 'X'), (7, 'X'), (9, 'X'), (15, 'X'), (16, 'X'), (19, 'O'), (20, 'X'), (21, 'X'), (23, 'O'), (24, 'X'))
        # Test cases: test_lines
        tests = [ ((0,'X'), (0,'X')),                      # Repeat
                  
                  ((size+1,'O'),(size*size -1,'O')),       # Positive Diagonal
                  
                  ((size-1,'X'),(size*size - size, 'X')),  # Negative Diagonal

                  ((0,'X'), (1,'X'),(2,'X'), (4,'X')),     # Several in row

                  ((0,'X'), (10,'X'), (15,'X'), (20,'X')), # Several in column                  
                  
                  tuple( (u, ran.choice(['X','O']) ) for u in 
                          
                          set([ ran.randint(0,size*size - 1) for _ in range(3*size)]) ) #random sequence of unique moves
                  
                  ]
        
        # Test Grid
        for t, test in enumerate(tests):
            grid = [ [' ' for i in range(size)] for j in range(size) ]
            for p in test:
                x, y = p[0]%size, p[0]//size
                grid[y][x] = p[1]


            #####Test#####
            print "Test: ", t, test            
            print
            for row in grid:
                print row

            print
            lns = self.findLines(test)
            for direction in lns:
                lines = { coord : lns[direction][coord] for coord in lns[direction] if lns[direction][coord] is not None }
                print direction, [(line, lns[direction][line]) for line in lines if len(lns[direction][line]) > 1]
            # print
            # print "O's"
            # lns = self.findLines(test, 'O')
            # for l in lns: 
            #     print l, lns[l]
            # print '----- end ', t
            # print
