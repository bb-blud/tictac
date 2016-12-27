from random import randint
from game_board import GameBoard
from game_state import Player, GameState, QMap

class LearningPlayer(Player):
    def __init__(self, mark, game_state, policy):
        super(LearningPlayer, self).__init__(mark, game_state)
        self.policy = policy

    def makeMove(self):
        gs = self.game_state
        
        move = {
            'random' : self.randomMove,
            'maximize' : None,
            'minimize' : None }[self.policy]()

        return move
    
    def randomMove(self):
        size = self.game_state.size
        valid = False
        move_index = None
        while not valid:
            move_index = randint(0, size**2 - 1)
            valid = self.game_state.validMove(move_index)
            
        return move_index, self.mark
            
def run():

    ##### Initialize #####
    cummulativeQ = QMap()
    gs = GameState(3)
    gs.setPlayers(LearningPlayer('X', gs, 'random') ,LearningPlayer('O', gs, 'random' ) )

    ##### Play Games #####
    n_games = 1
    for game in range(n_games):
        gs.setQMap(cummulativeQ)     
        while not gs.game_finished:
            gs.takeStep()
            gs.printGrid(gs.makeGrid(gs.game_sequence))
            print
        for p in gs.players:
            print p.mark, "is winner: ", p.is_winner
        cummulativeQ = gs.getQMap()
        gs.resetGame()

    ##### Explore results #####
    Q = cummulativeQ.getQ()
    M = max(seq[0] for seq in Q.keys())

    for k in range(1,M):
        print "Explored Moves at step", k
        explored = (moves for moves in Q if moves[0] == k)
        for seq in explored:
            print seq, Q[seq]
        print

    ## Tests ##
    #Find lines
    # s = GameState(5)
    # s.test_lines()
    
    # #Transform to 'standard' position
    # gs = GameState()
    # gs.testTransform()
    
    
if __name__ == '__main__':
    run()
