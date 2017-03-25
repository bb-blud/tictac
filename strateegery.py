"""
This module contains all game strategy logic used by the player agents.
5 main game strategies exist, 
* random
* human (prompts for user input),
* ideal (hardcoded logic)
* Qlearning (learned Q map based decisions)
* minimax
  i) Hardcoded node evaluation using minmaxMeasure
 ii) Q map based node evaluation

"""
import random

debug = False
seed = 01162017
random.seed(seed)

class Strateegery(object):
    
    def __init__(self, game_state):
        self.game_state = game_state
        self.human_move_index = 0  # Default upper left corner

        
    def linesOfRankN(self, N, sequence, player):
        """
        Workhorse method returns all lines in the current game that have length or "rank" N

        """
        gs = self.game_state
        size = gs.size
        lines = gs.findLines(sequence)
        n_ranked = []

        for direction in lines:
            keys = range(size)
            if direction in ['D-pos', 'D-neg']:
                keys = [0] # There is only one line for each diagonal, so only one index to reference

            viables = [coord for coord in keys if lines[direction].get(coord, "Empty") not in ["Empty", None]]
            
            for line in (lines[direction][coord] for coord in viables):
                # If the line belongs to the player  and its length is N 
                if line[0] == player.mark and len(line) - 1 == N: #(first entry is player's mark not index hence minus 1)
                    n_ranked.append((direction, line))
                    
        return n_ranked

    ###########################################################
    # Human player 
    ###########################################################
    def humanMove(self, player):
        gs = self.game_state
        
        return self.human_move_index , player.mark
        ### Interactive in terminal
        # choosing = True
        # gs.printGrid(gs.makeGrid(gs.game_sequence))
        # while choosing:
        #     index = input("type index of your next move: ")
        #     if index in range(gs.size**2) and gs.validMove(index, gs.game_sequence):
        #         return index, player.mark
        #     else:
        #         print "Thats an invalid move"
                     
    ###########################################################
    # Random strategy
    ###########################################################
    def randomMove(self, player):
        size = self.game_state.size
        valid = False
        move_index = None
        while not valid: # Take take random index until it is valid
            move_index = random.randint(0, size**2 - 1)
            valid = self.game_state.validMove(move_index, self.game_state.game_sequence)
            
        return move_index, player.mark
    
    ###########################################################
    # Q-Learning learning
    ###########################################################
    def Qlearning(self, player, threshold = .3):
        gs = self.game_state
        t_sequence = tuple( (gs.transformIndex(i), m) for i,m in gs.game_sequence )
        Q = gs.QM.Q
        if player.use_inner_Q:
            Q = player.inner_Q.Q

        # All indices that are legal next moves
        valid_indices= [ index for index in range(gs.size**2) if gs.validMove(index, t_sequence) ]

        # Player 1 will choose to maximize, Player 2 will minimize
        player_strategy = { gs.players[0].mark : max, gs.players[1].mark : min } [player.mark]
        
        # Visited sequences in Q that match the current game up until their last move (i.e. possible futures after current state)
        charted = [ seq for seq in Q.keys() if seq[:-1] == tuple(t_sequence) ]
        
        # Legal moves that lead to sequences not in Q yet
        uncharted_i = [ index for index in valid_indices if index not in [ seq[-1][0] for seq in charted ] ]

        if uncharted_i and random.random() > threshold and gs.step > 1: # If a move hasn't been done try it, randomly
            #print 'uncharted'
            return gs.inverseTFIndex(random.choice(uncharted_i)), player.mark
        
        # Q index and values of the future sequences that could be legally taken
        index_and_val = { c : Q[c] for c in charted if c[-1][0] in valid_indices}
        
        if index_and_val:
            #print 'optimize', player_strategy([1,9]), player.mark #debug
            player_optimal = player_strategy(index_and_val, key=Q.get)
            equivalents = [c for c in index_and_val if Q[c] == Q[player_optimal] ] # There might be more that one sequence that is optimal
            move_seq = random.choice(equivalents)
            return gs.inverseTFIndex(move_seq[-1][0]) , player.mark
        
        #print 'just valid' #debug
        return gs.inverseTFIndex(random.choice(valid_indices)) , player.mark # simply return a legal move in any other case
            
            
    ###########################################################
    # MiniMax alpha-beta pruning and supporting functions
    ###########################################################

    def isLeaf(self, sequence, player):
        gs = self.game_state        
        return {
            'tie': gs.isTie(sequence),
            'win': len(self.linesOfRankN(gs.size, sequence, player)) > 0} # True if there is a line of length size, game over
    
    def minimaxMeasure(self, sequence, player, isleaf):
        gs = self.game_state
        size = self.game_state.size
        
        # If current node is an endgame tie
        if isleaf['tie']:     
            return 0
        # If current node is an endgame win
        elif isleaf['win']:   
            sgn = {gs.players[0].mark : 1, gs.players[1].mark : -1}[player.mark]
            return sgn * (10*size)**4 * len(self.linesOfRankN(size, sequence, player))  # reward max/min for a player win
        else:
            measure = 0 
            for n in range(1,size):
                measure += n * len(self.linesOfRankN(n, sequence, gs.players[0]))  # game measure max player
            for n in range(1,size):
                measure -= n * len(self.linesOfRankN(n, sequence, gs.players[1]))  # game measure min player
            return measure

    ##### miniQmax #####
    def miniQMax(self, sequence, player, isleaf):
        gs = self.game_state
        set_val = False
        
        sgn = {gs.players[0].mark : 1.0, gs.players[1].mark : -1.0}[player.mark]
        t_seq = tuple( (gs.transformIndex(i), mark) for i,mark in sequence )
        val = gs.QM.Q.get(t_seq, None)
        
        if val is None and gs.learning:
            set_val = True  # If learning is on (during training) values are set to Q and returned

        # If current node is an endgame tie return 0
        if isleaf['tie']:            
            if set_val:  
                gs.QM.Q[t_seq] = 0 # Setting value if learning
            return 0
        
        # If current node is an endgame is a win return +-1
        elif isleaf['win']:
            if set_val:
                gs.QM.updateQ(t_seq ,sgn)
            return sgn  
        else:
            # return zero of reached unexplored state (code is set for possible return of experimental values)
            if val is None:  
                if set_val:
                    gs.QM.Q[t_seq] = sgn * 0.
                return sgn*0.
            else:
                return val # If node is not a leaf then return the Q's value for it
        
    #### minimax #####
    def minimax(self, sequence, depth, Min, Max, player, evaluate):
        gs = self.game_state
        size = gs.size
        opponent = [p for p in gs.players if p.mark is not player.mark][0]
        
        isleaf = self.isLeaf(sequence,player)
        
        if isleaf['tie'] or isleaf['win'] or depth == 0:  # If we have reached depth limit or we are at a leaf node
            return evaluate(sequence, player, isleaf)

        valid_i = [ index for index in range(size**2) if gs.validMove(index, sequence) ]
        ## Max 
        if  player == gs.players[0]:
            v = Min
            for i in valid_i:
                child_seq = sequence[:] + [(i, player.mark)]
                v_c = self.minimax(child_seq, depth-1, v, Max, opponent, evaluate)
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
                v_c = self.minimax(child_seq, depth-1, Min, v, opponent, evaluate)
                if v_c < v:
                    v = v_c
                if v < Min:
                    return Min
            return v

    def minimaxMove(self, player, depth):
        gs = self.game_state
        size = gs.size
        opponent = gs.otherPlayer()
        
        valid_indices = [ index for index in range(size**2) if gs.validMove(index, gs.game_sequence) ]
        optimal = {gs.players[0].mark : max, gs.players[1].mark : min}[player.mark]

        evaluate, Min, Max = { 'miniQmax' : (self.miniQMax, -0.5, 0.5),
                               'minimax'  : (self.minimaxMeasure, -size, size) }[player.policy]
        moves = []
        for i in valid_indices:
            move = (i, player.mark)
            mm = self.minimax(gs.game_sequence[:] + [move], depth, Min, Max, opponent, evaluate)
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
        # Legal future moves that can be taken
        valid_indices = [ index for index in range(size**2) if gs.validMove(index, gs.game_sequence) ]
        opponent = gs.otherPlayer()

        # Corner opening move tends to be stronger, hardcoded here
        if gs.step == 1:
            return random.choice([0,size-1,size**2-1,size**2-size]), player.mark

        # 1st priority, Block opponent from winning or win game
        # 
        for strategy in ['gain', 'block']: 
            p = {'block' : opponent, 'gain' : player}[strategy]

            for i in valid_indices:                             
                test_seq = gs.game_sequence[:] + [(i, p.mark)]   

                full_line = self.linesOfRankN(size, test_seq, p)
                if full_line != []: # If there is a 
                    return i, player.mark        

        if gs.step >= 4*size - 9:  # Check only when game is sufficiently developed

            # 2nd priority, Block opponent's fork or fork
            #
            for strategy in ['gain', 'block']:
                p = {'block' : opponent, 'gain' : player}[strategy] 
                
                for i in valid_indices:
                    test_seq = gs.game_sequence[:] + [(i, p.mark)]    # Find lines that are one move away from a
                    forks = self.linesOfRankN(size - 1, test_seq, p)  # win in every possible next sequence

                    if forks != [] and len(forks) >=2:  # If a sequence yields two such lines then a fork will exist on next move
                        if strategy == 'block':         # If fork will belong to the opponent set up a block
                            
                            # We are one move away from a fork, one more away from opponent's win
                            # Our options lie two moves from end, consider lines of size - 2
                            block_lines = self.linesOfRankN(size - 2, gs.game_sequence,  player) 
                            
                            for index in valid_indices: 
                                for b_line in block_lines:
                                    
                                    # consider valid next moves belonging to such potential block lines
                                    if gs.belongsToLine(index, b_line[0], b_line[1]):
                                        
                                        # if we take a position in the block line (making it of length size -1)
                                        # which index makes it of length size, (i.e. a winning line)
                                        index_to_win = gs.indexToWin(b_line[0], b_line[1] + [index])

                                        # Suppose the opponent blocks our win, hence the following sequence;
                                        block_fork_seq = test_seq + [(index, player.mark),(index_to_win, opponent.mark)]

                                        # We don't want the opponent's block, to actually form his fork OR give him a win
                                        if len(self.linesOfRankN(size, block_fork_seq, opponent)) < 1 and \
                                           len(self.linesOfRankN(size - 1, block_fork_seq, opponent))< 2:  #no opponent wins and no opponent forks 
                                        
                                            # Opponent blocking our line will now ruin his fork attempt, 
                                            return index, player.mark
                                        
                        if strategy == 'gain':
                            # Otherwise next fork is current player's, make it
                            return i, player.mark
                            
        # Else measure the value of each possible next move
        #
        index_measures = {'block':{}, 'gain':{}} 
        for strategy in ['gain', 'block']:
            p = {'block' : opponent, 'gain' : player}[strategy]
        
            for i in valid_indices:
                test_seq = gs.game_sequence[:] + [(i, p.mark)]
                #For every possible next move measure the state of the game
                #in terms of current player AND from opponent's perspective
                measure_at_i = self.measureState(test_seq, p)
                index_measures[strategy][i] = measure_at_i

        # Which next move gives the biggest value for opponent (even if its not his move next)
        max_block_index = max(index_measures['block'], key=index_measures['block'].get)
        # Which next move gives the biggest value for current player
        max_gain_index = max(index_measures['gain'], key=index_measures['gain'].get)

        # Return move of most measure or block the opponent's
        #
        #Make move of highest measure if its measure is bigger than or equal to opponents highest measure
        if index_measures['gain'][max_gain_index] >= index_measures['block'][max_block_index]:
            if debug:
                print "measure gain", max_gain_index, player.mark
            return max_gain_index, player.mark
        
        #Else opponent can gain more value with his max move than current player
        #Prevent him from taking it
        else:
            if debug:
                print "measure block", max_block_index, player.mark
            return max_block_index, player.mark
