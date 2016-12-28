#from __future__ import print_function

class Strateegery(object):
    def __init__(self, game_state):
        self.game_state = game_state
        
    def measureState(self):
        gs = self.game_state
        size = self.game_state.size
        X_weight = 0
        O_weight = 0
        state_weight = 0
        for direction in gs.lines:

            keys = range(size)
            if direction == 'Diagonal':
                keys = ['pos', 'neg']
                
            viables = (coord for coord in keys if  gs.lines[direction].get(coord, "Empty") not in ["Empty", None])
            
            for line in (gs.lines[direction][coord] for coord in viables):
                if line[0] == 'X' and len(line[1:]) > 1:
                    X_weight += len(line[1:])
                if line[0] == 'O' and len(line[1:]) > 1:
                    O_weight += len(line[1:])
        
        print "X_weight: ", X_weight
        print "O_weight: ", O_weight
        print
                
        return X_weight, "working on it"
