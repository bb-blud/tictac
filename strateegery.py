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
            if direction in ['D-pos', 'D-neg']:
                keys = [0]
                
            viables = [coord for coord in keys if  lines[direction].get(coord, "Empty") not in ["Empty", None]]
            
            for line in (lines[direction][coord] for coord in viables):
                if line[0] == player.mark and len(line) - 1 == N: # first entry is mark
                    n_ranked.append((direction, line))
                    
        return n_ranked


    ###########################################################
    # Random strategy
    ###########################################################
    def randomMove(self, player):
        size = self.game_state.size
        valid = False
        move_index = None
        while not valid:
            move_index = randint(0, size**2 - 1)
            valid = self.game_state.validMove(move_index, self.game_state.game_sequence)
            
        return move_index, player.mark        

    ##########################################################
    # MiniMax alpha-beta pruning and supporting functions
    ##########################################################
    def minimaxMeasure(self, sequence, player):
        gs = self.game_state
        size = self.game_state.size
        measure = 0
        
        if gs.isTie(sequence):
            return 0
        
        for n in range(1,size):
            measure += n * len(self.linesOfRankN(n, sequence, gs.players[0]))
        for n in range(1,size):
            measure -= n * len(self.linesOfRankN(n, sequence, gs.players[1]))
            
        # reward max/min for a player win
        sgn = {gs.players[0].mark : 1, gs.players[1].mark : -1}[player.mark]
        measure += sgn * size**4 * len(self.linesOfRankN(size, sequence, player))
            
        return measure
        
    def isLeaf(self, sequence, player):
        gs = self.game_state        
        if gs.isTie(sequence):
            return True
        if len(self.linesOfRankN(gs.size, sequence, player)) > 0:
            return True
        
    def minimax(self, sequence, depth, Min, Max, player):
        gs = self.game_state
        size = gs.size

        if self.isLeaf(sequence, player) or depth == 0:
            return self.minimaxMeasure(sequence, player)

        valid_indices = [ index for index in range(size**2) if gs.validMove(index, sequence) ]
        ## Max
        if  player == gs.players[0]:  
            v = Min
            for i in valid_indices:
                child_seq = sequence[:] + [(i, player.mark)]
                v_c = self.minimax(child_seq, depth-1, v, Max, player)
                if v_c > v:
                    v = v_c
                if v > Max:
                    return Max
            return v
        ## Min
        else:                         
            v = Max
            for i in valid_indices:
                child_seq = sequence[:] + [(i, player.mark)]
                v_c = self.minimax(child_seq, depth-1, Min, v, player)
                if v_c < v:
                    v = v_c
                if v < Min:
                    return Min
            return v

    def minimaxMove(self, player):
        gs = self.game_state
        size = gs.size
        valid_indices = [ index for index in range(size**2) if gs.validMove(index, gs.game_sequence) ]

        moves = []
        for i in valid_indices:
            move = (i, player.mark)
            mm = self.minimax(gs.game_sequence + [move], 3 , -200, 200, player)
            moves.append([mm, move])
        return moves
                    
    ##########################################################
    # Original attempt at an optimal ('ideal') strategy
    ##########################################################
    
    def measureState(self, sequence, player):
        state_weight = 0
        for n in range(1,self.game_state.size):
            state_weight += n * len(self.linesOfRankN(n, sequence, player))
        return state_weight

    def ideal(self, player):
        gs = self.game_state
        size = gs.size
        valid_indices = [ index for index in range(size**2) if gs.validMove(index, gs.game_sequence) ]
        opponent = gs.otherPlayer()

        print gs.step

        if gs.step >= 4*size - 9:  # Only check when game is sufficiently developed

            # 1st priority, Block opponent from winning or win game                                                     
            # 
            for strategy in ['gain', 'block']:
                p = {'block' : opponent, 'gain' : player}[strategy]

                for i in valid_indices:                             
                    test_seq = gs.game_sequence[:] + [(i, p.mark)]   

                    full_line = self.linesOfRankN(size, test_seq, p)
                    if full_line != []:
                        print "win/block", i, player.mark, strategy
                        return i, player.mark

            # 2nd priority, Block opponent's fork or fork
            #
            for strategy in ['gain', 'block']:
                p = {'block' : opponent, 'gain' : player}[strategy]

                for i in valid_indices:
                    test_seq = gs.game_sequence[:] + [(i, p.mark)]

                    forks = self.linesOfRankN(size - 1, test_seq, p)

                    if forks != [] and len(forks) >=2:

                        if strategy == 'block':
                            block_lines = self.linesOfRankN(size - 2, test_seq,  player)

                            for index in (k for k in valid_indices if k is not i):
                                for b_line in block_lines:
                                    
                                    if gs.belongsToLine(index, b_line[0], b_line[1]):
                                        index_to_win = gs.indexToWin(b_line[0], b_line[1] + [index])
                                        block_fork_seq = test_seq + [(index, player.mark),(index_to_win, opponent.mark)]
                                        
                                        if len(self.linesOfRankN(size - 1, block_fork_seq, opponent)) < 2: # No forks any longer
                                            return index, player.mark
                                        
                        if strategy == 'gain':
                            print "fork", i, player.mark, strategy
                            return i, player.mark
                            
        # Else measure the value of each possible next move
        #
        index_measures = {'block':{}, 'gain':{}}
        for strategy in ['gain', 'block']:
            p = {'block' : opponent, 'gain' : player}[strategy]
        
            for i in valid_indices:
                test_seq = gs.game_sequence[:] + [(i, p.mark)]

                measure_at_i = self.measureState(test_seq, p)
                index_measures[strategy][i] = measure_at_i

        max_block_index = max(index_measures['block'], key=index_measures['block'].get)
        max_gain_index = max(index_measures['gain'], key=index_measures['gain'].get)
        
        print index_measures['block']                            #
        print index_measures['gain']                             #
        print 'at indicies: ', max_block_index, max_gain_index   # Debug
        
        # Return move of most measure or block the opponent's
        #
        if index_measures['gain'][max_gain_index] >= index_measures['block'][max_block_index]:  
            print "measure gain", max_gain_index, player.mark
            return max_gain_index, player.mark
        else:
            print "measure block", max_block_index, player.mark
            return max_block_index, player.mark
        







        
# print forks
# print block_lines
# print [index for index in (k for k in valid_indices if k is not i)]
