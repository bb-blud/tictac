import random as ran
class GameState(object):

    def __init__(self, size=3):
        self.size = size

    def findLines(self, sequence, tac):
        lines = {}
        size = self.size

        for i, point1 in enumerate(sequence):
            for point2 in sequence[i+1:]:

                x1, x2 = point1[0] % size, point2[0] % size
                y1, y2 = point1[0] // size, point2[0] // size

                key = None
                if x1 == x2 and y1 == y2: #This case should not occur unless a bug
                    print "Error: A position has been played twice in the sequence"
                    print point1, point2
                    continue
                if x1 == x2:
                    key = ('c', x1)
                if y1 == y2:
                    key = ('r', y1)
                if x1 == y1 and x2 == y2:
                    key = ('d', 1)
                if x1+y1 == size-1 and x2+y2==size-1:
                    key = ('d', -1)

                if point1[1] == tac and point2[1] == tac:
                    if key and key not in lines:
                        lines[key] = [point1]
                    elif key and lines[key] != None:
                        lines[key].append(point2)
                elif key:
                    lines[key] = None

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
            print "X's"
            lns = self.findLines(test, 'X')
            for l in lns: 
                print l, lns[l]
            print
            print "O's"
            lns = self.findLines(test, 'O')
            for l in lns: 
                print l, lns[l]
            print '----- end ', t
            print
