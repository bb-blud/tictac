from random import randint

class Strateegery(object):
    def __init__(self, game_state):
        self.game_state = game_state
        
    def measureState(self, sequence):
        gs = self.game_state
        size = gs.size
        lines = gs.findLines(sequence)
        state_weight = 0

        win = 2*(size+1)*size
        player  = gs.current_player
        oponent = gs.otherPlayer()#[p for p in gs.players if p is not player][0]
        playerW  = 0
        oponentW = 0
        
        for direction in lines:
            keys = range(self.game_state.size)
            if direction == 'Diagonal':
                keys = ['pos', 'neg']
                
            viables = [coord for coord in keys if  lines[direction].get(coord, "Empty") not in ["Empty", None]]

            for line in (lines[direction][coord] for coord in viables):
                if line[0] == player.mark:
                    if len(line[1:]) == size:
                        playerW += win
                    else:
                        playerW += len(line[1:])
                        
                if line[0] == oponent.mark:
                    if len(line[1:]) == size:
                        oponentW += win
                    else:
                        oponentW += len(line[1:])
                        
        return playerW, oponentW
            # for line in (lines[direction][coord] for coord in viables):
            #     if line[0] == gs.players[0].mark:
            #         if len(line[1:]) == size:
            #             state_weight += win
            #         else:
            #             state_weight += len(line[1:])
                        
            #     if line[0] == gs.players[1].mark:
            #         if len(line[1:]) == size:
            #             state_weight -= win
            #         else:
            #             state_weight -= len(line[1:])
                
            # return state_weight

    def optimize(self, player):
        gs = self.game_state
        size = gs.size
        valid_indicies = [ index for index in range(size**2) if gs.validMove(index)]

        gains = {}
        for i in valid_indicies:
            test_seq = gs.game_sequence[:]
            test_seq.append( (i, player.mark) )
            gains[i] = self.measureState(test_seq)[0]

        other_player = gs.otherPlayer() #[p for p in gs.players if p is not player][0]
        blocks = {}
        for i in valid_indicies:
            test_seq = gs.game_sequence[:]
            test_seq.append( (i, other_player.mark) )
            blocks[i] = self.measureState(test_seq)[1]

        max_gain_index = max(gains, key=gains.get)
        max_block_index= max(blocks, key=blocks.get)
        

        print "current player: ", player.mark
        #print other_player.mark,': ',  blocks[max_block_index], player.mark,': ', gains[max_gain_index]
        print blocks
        print gains
        print 'at indicies: ', max_block_index, max_gain_index
        gs.printGame()
        print

        
        if gains[max_gain_index] >= blocks[max_block_index]:
            return max_gain_index, player.mark
        else:
            return max_block_index, player.mark
        
            
    # def optimize(self, player):
    #     gs = self.game_state
    #     size = gs.size

    #     optimum = { 'maximize' : max,
    #                 'minimize' : min }[player.policy]
        
    #     valid_moves = [ (index, player.mark) for index in range(size**2) if gs.validMove(index)]

    #     measures = {}
    #     for move in valid_moves:
    #         test_seq = self.game_state.game_sequence[:]
    #         test_seq.append(move)
    #         measures[move[0]] = self.measureState(test_seq)
        
    #     return optimum(measures, key=measures.get), player.mark

    def randomMove(self, player):
        size = self.game_state.size
        valid = False
        move_index = None
        while not valid:
            move_index = randint(0, size**2 - 1)
            valid = self.game_state.validMove(move_index)
            
        return move_index, player.mark    
