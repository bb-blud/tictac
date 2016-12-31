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
            'maximize' : self.strategies.optimize,
            'minimize' : self.strategies.optimize,            
            'debug'    : self.debug}[self.policy](self)

#        print self.strategies.measureState(self.game_state.game_sequence)
        return move
    
    ########## Player for debugging ##########
    def setDebug(self, sequence):
        from collections import deque
        self.inDebug = True
        self.problem_sequence = sequence
        self.Xmoves = deque([move for move in self.problem_sequence if move[1] == 'X'])
        self.Omoves = deque([move for move in self.problem_sequence if move[1] == 'O'])
        
    def debug(self, player):
        self.strategies.optimize(self)
        if self.inDebug:
            if self.mark == 'X':
                return self.Xmoves.popleft()
            if self.mark == 'O':
                return self.Omoves.popleft()
        return

        
def run():
    # ##### Initialize #####
    # cummulativeQ = QMap()
    # gs = GameState(3)
    # gs.setPlayers(LearningPlayer('X', gs, 'random') ,LearningPlayer('O', gs, 'minimize' ) )

    # ##### Play Games #####
    # n_games = 1
    # for game in range(n_games):
    #     gs.setQMap(cummulativeQ)     
    #     while not gs.game_finished:
    #         gs.takeStep()
    #         gs.printGame()

    #     for p in gs.players:
    #         print p.mark, "is winner: ", p.is_winner
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

############# Tests ###################
    
    # Debug game
    cummulativeQ = QMap()    
    gs = GameState(3)
    gs.setQMap(QMap())
    gs.setPlayers(LearningPlayer('X', gs, 'minimize'), LearningPlayer('O', gs, 'minimize'))
    #problem_sequence =  [(1,'X'), (6, 'O'), (7,'X'), (4, 'O'), (8,'X'), (2, 'O'), (3, 'X'), (5, 'O'), (0, 'X')]   # problems with diag
    #problem_sequence = [(0,'X'),(7,'O'),(3,'X'),(6,'O'),(4,'X'),(8,'O'),(2,'X'),(1,'O'),(5,'X')] # problems horizontal tally
    #problem_sequence = [(4, 'X'), (0,'O'), (1,'X'), (6, 'O'), (3, 'X'), (5, 'O'), (7, 'X')]  # Optimize fail (X-random, O-minimize)
    #problem_sequence =  [(2, 'X'), (4, 'O'), (6, 'X'), (0, 'O'), (8, 'X'), (5, 'O'), (7, 'X')]# Corner powned
    gs.setGameSequence([(2, 'X'), (4, 'O'), (6, 'X')]) # Corner powned
    # gs.setCurrentPlayer(gs.players[1])
    # problem_sequence  =[(0, 'O'), (8, 'X'), (5, 'O'), (7, 'X')]  # Corner powned

    #gs.setGameSequence([(2, 'X')])
    gs.setCurrentPlayer(gs.players[1])

    #gs.players[0].setDebug(problem_sequence)
    #gs.players[1].setDebug(problem_sequence)

    while not gs.game_finished:
        gs.takeStep()
    gs.printGame()
    ################
    
    # # Find lines
    # s = GameState(5)
    # s.test_lines()
    
    # #Transform to 'standard' position
    # gs = GameState()
    # gs.testTransform()
    
if __name__ == '__main__':
    run()
