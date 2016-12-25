from random import randint
from game_board import GameBoard
from game_state import Player, GameState, QMap

class LearningPlayer(Player):
    def __init__(self, mark, game_state):
        super(LearningPlayer, self).__init__(mark, game_state)

    def makeMove(self):
        size = self.game_state.size
        choosing = True
        move = None
        while choosing:
            move = randint(0, size**2 - 1)
            if move not in (m[0] for m in  self.game_state.game_sequence ):
                choosing = False
        return move, self.mark
            
def run():

    # ##### Initialize #####
    # cummulativeQ = QMap()
    # gs = GameState(3)
    # gs.setPlayers(LearningPlayer('X',gs) ,LearningPlayer('O',gs) )

    # ##### Play Games #####
    # n_games = 3
    # for game in range(n_games):
    #     gs.setQMap(cummulativeQ)     
    #     while not gs.gameFinished():
    #         gs.takeStep()
    #     cummulativeQ = gs.getQMap()
    #     gs.resetGame()

    # ##### Explore results #####
    # Q = cummulativeQ.getQ()
    # M = max(seq[0] for seq in Q.keys())

    # for k in range(1,M):
    #     print "Explored Moves at step", k
    #     explored = (moves for moves in Q if moves[0] == k)
    #     for seq in explored:
    #         print seq, Q[seq]
    #     print

    ## Tests ##
    #Find lines
    # s = GameState(5)
    # s.test_lines()
    
    #Transform to 'standard' position
    gs = GameState()
    gs.testTransform()
    
    
if __name__ == '__main__':
    run()
