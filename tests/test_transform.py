import sys
sys.path.append("../")

from utilities import *

##################################
# Test global coordinate transform
##

def testTransform(game):
        
    tests = [
        [3, 2, (2, 'O')],  #  
        [3, 8, (8, 'O')],  # All corners are equivalent
        [3, 6, (6, 'O')],  #

        [5, 12, (12, 'X')], # Center point doesn't move
        
        [4, 10, (10,'1'),(2,'2'),(3,'3'),(7,'4'),(11,'5')],  # Order is preserved

        [3, 3, (3, 'X')],

        [3, 7, (7, 'X')] ]  

    for i, test in enumerate(tests):
        game.resetGame()
            
        print "Test: ", i
        game.size = test[0]
        start = test[1]
        game.setTransform(start)

        point = game.getCoordinates(start)
        print "point: {}, Index: {}".format(point, start)
        print "tpoint: {}, Index: {}".format(game.transform(point), game.getIndex(game.transform(point)) )
        print
            
        seq = test[2:]
        print seq
        for row in game.makeGrid(seq):
            print row


        print
        tseq = [(game.transformIndex(s[0]), s[1]) for s in seq]
        print tseq
        for row in game.makeGrid(tseq):
            print row
            
        print
        ttseq = [(game.inverseTFIndex(s[0]), s[1]) for s in tseq]
        print ttseq
        for row in game.makeGrid(ttseq):
            print row
        print 'END Test: ', i
        
if __name__ == "__main__":
    game = GameState()
    testTransform(game)
