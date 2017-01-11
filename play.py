from game_board import GameBoard
from game_state import Player, GameState, QMap
from strateegery import Strateegery

class LearningPlayer(Player):
    def __init__(self, mark, game_state, policy):
        super(LearningPlayer, self).__init__(mark, game_state)
        self.policy = policy
        self.strategies  = Strateegery(self.game_state)
        
    def makeMove(self):
        move = {
            'random'   : self.strategies.randomMove,
            'minimax'  : self.strategies.minimaxMove,
            'ideal'    : self.strategies.ideal,
            'debug'    : self.debug}[self.policy](self)

        return move
    
    ########## Player for debugging ##########
    def setDebug(self, sequence):
        from collections import deque
        self.inDebug = True
        self.problem_sequence = sequence
        self.Xmoves = deque([move for move in self.problem_sequence if move[1] == 'X'])
        self.Omoves = deque([move for move in self.problem_sequence if move[1] == 'O'])
        
    def debug(self, player):
        self.strategies.ideal(self)
        if self.inDebug:
            if self.mark == 'X':
                return self.Xmoves.popleft()
            if self.mark == 'O':
                return self.Omoves.popleft()
        return

def run():
    ##### Initialize #####
    cummulativeQ = QMap()
    gs = GameState(3)
    gs.setPlayers(LearningPlayer('X', gs, 'random'), LearningPlayer('O', gs, 'random' ) )

    ##### Play Games #####
    n_games = 10
    for game in range(n_games):
        gs.setQMap(cummulativeQ)     
        while not gs.game_finished:
            gs.takeStep()
#            gs.printGame()
#       gs.printGame()

        for p in gs.players:
            print p.mark, "is winner: ", p.is_winner
        cummulativeQ = gs.getQMap()
        gs.resetGame()

    ##### Explore results #####
    Q = cummulativeQ.getQ()
    M = max(len(seq) for seq in Q.keys())

    for k in range(1,M):
        print "Explored Moves at step", k
        explored = (moves for moves in Q if len(moves) == k)
        for seq in explored:
            print seq, Q[seq]
        print

############# Tests ###################
    
#     # Debug game
#     cummulativeQ = QMap()    
#     gs = GameState(3)
#     gs.setQMap(QMap())
#     gs.setPlayers(LearningPlayer('X', gs, 'debug'), LearningPlayer('O', gs, 'ideal'))
#     #problem_sequence =  [(1,'X'), (6, 'O'), (7,'X'), (4, 'O'), (8,'X'), (2, 'O'), (3, 'X'), (5, 'O'), (0, 'X')]   # problems with diag
#     #problem_sequence = [(0,'X'),(7,'O'),(3,'X'),(6,'O'),(4,'X'),(8,'O'),(2,'X'),(1,'O'),(5,'X')] # problems horizontal tally
#     #problem_sequence = [(4, 'X'), (0,'O'), (1,'X'), (6, 'O'), (3, 'X'), (5, 'O'), (7, 'X')]  # Optimize fail (X-random, O-minimize)
#     #problem_sequence =  [(2, 'X'), (4, 'O'), (6, 'X'), (0, 'O'), (8, 'X'), (5, 'O'), (7, 'X')]# Corner powned
#     #problem_sequence  =[(0, 'O'), (8, 'X'), (5, 'O'), (7, 'X')]  # Corner powned
#     #problem_sequence = [(4,'X'), (0, 'O'), (5, 'X'), (3, 'O'), (8, 'X'), (2, 'O'), (1, 'X'), (7, 'O'), (6, 'X')] #blocking instead of winning
#     #problem_sequence = [(5, 'X'), (4, 'O'), (8, 'X'), (2, 'O'), (6, 'X'), (1, 'O'), (7, 'X')] # not blocking

#     problem_sequence = [(4, 'X'), (0, 'O'), (8, 'X')] # Division by 0 error in indexInLine, diagonal fork
#     gs.players[0].setDebug(problem_sequence)
# #    gs.setGameSequence(problem_sequence)
# #    gs.setCurrentPlayer(gs.players[1])

    
#     # gs.setGameSequence([(7, 'X'), (4, 'O')]) #list index out of range
#     # gs.setCurrentPlayer(gs.players[0])
#     # gs.players[0].setDebug([(8, 'X')])
    
#     #gs.setGameSequence([(2, 'X')])
#     #gs.setCurrentPlayer(gs.players[1])

# #    gs.players[0].setDebug(problem_sequence)
# #    gs.players[1].setDebug(problem_sequence)

#     while not gs.game_finished:
#         gs.takeStep()
#         gs.printGame()
#     ################
    
    # # Find lines
    # s = GameState(5)
    # s.test_lines()
    
    # #Transform to 'standard' position
    # gs = GameState()
    # gs.testTransform()
    
if __name__ == '__main__':
    run()
