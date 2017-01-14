import random

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
                
            viables = [coord for coord in keys if lines[direction].get(coord, "Empty") not in ["Empty", None]]
            
            for line in (lines[direction][coord] for coord in viables):
                if line[0] == player.mark and len(line) - 1 == N: # first entry is a mark
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
            move_index = random.randint(0, size**2 - 1)
            valid = self.game_state.validMove(move_index, self.game_state.game_sequence)
            
        return move_index, player.mark
    
    ###########################################################
    # Reinforcement learning
    ###########################################################
    def reinforcement(self, player, threshold = .3):
        gs = self.game_state
        Q = gs.QMap.Q
        
        if Q == {} and gs.step == 1:
            print "empty dict"
            return random.choice([i for i in range(gs.size**2) if gs.validMove(i, gs.game_sequence)]), player.mark
        
        t_valids = [ gs.transformIndex(index) for index in range(gs.size**2) if gs.validMove(index, gs.game_sequence) ]
        
        strategies = { gs.players[0].mark : max, gs.players[1].mark : min }
                
        player_strategy = strategies[player.mark]

        charted = [ seq for seq in Q.keys() if len(seq) == gs.step]
 
        uncharted_i = [ index for index in t_valids if index not in [ seq[-1][0] for seq in charted ] ]

        # print 'game sequence: ',gs.game_sequence
        # print 'transfrom seq: ',[(gs.transformIndex(m[0]), m[1] ) for m in gs.game_sequence ]
        # print 'valids', t_valids
        # print
        # print 'charted', [seq[-1][0] for seq in charted]
        # print
        print 'uncharted', uncharted_i
       
        if uncharted_i and random.random() > threshold and gs.step > 1:
            print 'uncharted'
            return gs.transformIndex(random.choice(uncharted_i)), player.mark

        index_and_val = { c : Q[c] for c in charted if c[-1][0] in t_valids}
        
        if index_and_val:
            print 'optimize', player_strategy([1,9]), player.mark
            player_optimal = player_strategy(index_and_val, key=Q.get)
            return gs.transformIndex(player_optimal[-1][0]) , player.mark
        
        print 'just valid'        
        return gs.transformIndex(random.choice(t_valids) ), player.mark
            
            
    ###########################################################
    # MiniMax alpha-beta pruning and supporting functions
    ###########################################################
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
        measure += sgn * (10*size)**4 * len(self.linesOfRankN(size, sequence, player))
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
        opponent = [p for p in gs.players if p.mark is not player.mark][0]

        if self.isLeaf(sequence, player) or depth == 0:
            return self.minimaxMeasure(sequence, player)

        valid_i = [ index for index in range(size**2) if gs.validMove(index, sequence) ]
        ## Max
        if  player == gs.players[0]:
            v = Min
            for i in valid_i:
                child_seq = sequence[:] + [(i, player.mark)]
                v_c = self.minimax(child_seq, depth-1, v, Max, opponent)
                if v_c > v:
                    v = v_c
                if v > Max:
                    return Max
            return v
        ## Min
        else:
            v = Max
            for i in valid_i:
                child_seq = sequence[:] + [(i, player.mark)]
                v_c = self.minimax(child_seq, depth-1, Min, v, opponent)
                if v_c < v:
                    v = v_c
                if v < Min:
                    return Min
            return v

    def minimaxMove(self, player):
        gs = self.game_state
        size = gs.size
        opponent = gs.otherPlayer()
        
        valid_indices = [ index for index in range(size**2) if gs.validMove(index, gs.game_sequence) ]
        optimal = {gs.players[0].mark : max, gs.players[1].mark : min}[player.mark]

        moves = []
        for i in valid_indices:
            move = (i, player.mark)
            mm = self.minimax(gs.game_sequence[:] + [move], 2, -size*2, size*2, opponent)
            moves.append((mm, move))

        return optimal(moves)[1]
    
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

        if gs.step >= 4*size - 9:  # Check Only check when game is sufficiently developed

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
                                                            
                                        if len(self.linesOfRankN(size, block_fork_seq, opponent)) < 1 and \
                                        len(self.linesOfRankN(size - 1, block_fork_seq, opponent))< 2:    # No winning lines and no more forks
                                            
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

        # Return move of most measure or block the opponent's
        #
        if index_measures['gain'][max_gain_index] >= index_measures['block'][max_block_index]:  
            print "measure gain", max_gain_index, player.mark
            return max_gain_index, player.mark
        else:
            print "measure block", max_block_index, player.mark
            return max_block_index, player.mark
