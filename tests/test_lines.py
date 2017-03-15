import sys
sys.path.append("../")

import random as ran
from utilities import *

##################################
# Test findLines workhorse method
##

def testLines(game):
    size = game.size
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
        grid = game.makeGrid(test)

        #####Test#####
        print
        print "TEST: ", t, test            
        game.printGrid(grid)

        lines_in_seq = game.findLines(test)
        for direction in lines_in_seq:
            print direction
            print [ (l, lines_in_seq[direction][l]) for l in lines_in_seq[direction] if
                lines_in_seq[direction][l] is not None and len(lines_in_seq[direction][l]) >1 ]
        game.resetGame()
        print
        
if __name__ == "__main__":
    game = GameState(5)
    testLines(game)
