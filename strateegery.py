from random import randint

class Strateegery(object):
    def __init__(self, game_state):
        self.game_state = game_state

    def linesOfRankN(self, N, sequence, player):
        gs = self.game_state
        size = gs.size
        lines = gs.findLines(sequence)
        n_ranked = []

        for direction in lines:
            keys = range(size)
            if direction == 'Diagonal':
                keys = ['pos', 'neg']
                
            viables = [coord for coord in keys if  lines[direction].get(coord, "Empty") not in ["Empty", None]]
            for line in (lines[direction][coord] for coord in viables):
                if line[0] == player.mark and len(line[1:]) == N:
                    n_ranked.append((direction, line))
        return n_ranked
    
    def measureState(self, sequence, player):
        state_weight = 0
        for n in range(1,self.game_state.size):
            state_weight += n * len(self.linesOfRankN(n, sequence, player))
        return state_weight
    
    def ideal(self, player):
        gs = self.game_state
        size = gs.size
        valid_indicies = [ index for index in range(size**2) if gs.validMove(index) ]
        opponent = gs.otherPlayer()

        index_measures = {'block':{}, 'gain':{}}
        for strategy in ['block', 'gain']:
            p = {'block' : opponent,
                 'gain'  : player}[strategy]

            for i in valid_indicies:
                test_seq = gs.game_sequence[:]
                test_seq.append( (i, p.mark) )

                full_line = self.linesOfRankN(size, test_seq, p) #
                if full_line != []:                              # 1st, Block opponent from winning or win game
                    return i, player.mark

                forks = self.linesOfRankN(size - 1, test_seq, p) #
                if forks != [] and len(forks) >=2:               # 2nd, Block opponent's fork or fork
                    print "FORKS", forks
                    
                measure_at_i = self.measureState(test_seq, p)  
                index_measures[strategy][i] = measure_at_i

        max_block_index = max(index_measures['block'], key=index_measures['block'].get)
        max_gain_index = max(index_measures['gain'], key=index_measures['gain'].get)
        
        print index_measures['block']
        print index_measures['gain']
        print 'at indicies: ', max_block_index, max_gain_index
        
        if index_measures['gain'][max_gain_index] >= index_measures['block'][max_block_index]:
            return max_gain_index, player.mark
        else:
            return max_block_index, player.mark
        
    def randomMove(self, player):
        size = self.game_state.size
        valid = False
        move_index = None
        while not valid:
            move_index = randint(0, size**2 - 1)
            valid = self.game_state.validMove(move_index)
            
        return move_index, player.mark    
        
