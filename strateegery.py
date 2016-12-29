from random import randint

class Strateegery(object):
    def __init__(self, game_state):
        self.game_state = game_state
        
    def measureState(self, sequence):
        lines = self.game_state.findLines(sequence)
        state_weight = 0
        
        for direction in lines:
            keys = range(self.game_state.size)
            if direction == 'Diagonal':
                keys = ['pos', 'neg']
                
            viables = (coord for coord in keys if  lines[direction].get(coord, "Empty") not in ["Empty", None])
            
            for line in (lines[direction][coord] for coord in viables):
                if line[0] == 'X':
                    state_weight += len(line[1:])
                if line[0] == 'O':
                    state_weight -= len(line[1:])
                
        return state_weight

    def optimize(self, player):
        gs = self.game_state
        size = gs.size

        optimum = { 'maximize' : max,
                    'minimize' : min }[player.policy]
        
        valid_moves = [ (index, player.mark) for index in range(size**2) if gs.validMove(index)]

        measures = {}
        for move in valid_moves:
            test_seq = self.game_state.game_sequence[:]
            test_seq.append(move)
            measures[move[0]] = self.measureState(test_seq)
        
        return optimum(measures, key=measures.get), player.mark

    def randomMove(self, player):
        size = self.game_state.size
        valid = False
        move_index = None
        while not valid:
            move_index = randint(0, size**2 - 1)
            valid = self.game_state.validMove(move_index)
            
        return move_index, player.mark    
