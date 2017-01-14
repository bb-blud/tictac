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
            'reinforcement': self.strategies.reinforcement,
            'debug'    : self.debug}[self.policy](self)

        # self.strategies.reinforcement(self)
        # print
        print "RMOVE", move
        print
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


def playGames(cummulativeQ, game_state, policies, n_games):

    ##### Initialize #####
    gs = game_state
    gs.setPlayers(LearningPlayer('X', gs, policies[0]), LearningPlayer('O', gs, policies[1] ) )

    ##### Play Games #####
    for game in range(n_games):
        gs.setQMap(cummulativeQ)     
        while not gs.game_finished:
            gs.takeStep()
            print policies
            print [k for k in gs.QMap.Q.keys() if len(k) == 1] 
            gs.printGame()
        gs.printGame()
        print
        for p in gs.players:
            print p.mark, "is winner: ", p.is_winner
        cummulativeQ = gs.getQMap()
        gs.resetGame()
        
    return cummulativeQ

def run():


    # ##### Explore results #####
    # Q = cummulativeQ.getQ()
    # M = max(len(seq) for seq in Q.keys())

    QM = playGames(QMap(), GameState(4), ['random', 'random'], 70)

    QM = playGames(QM, GameState(4), ['reinforcement', 'reinforcement'], 1000)

    Q = QM.getQ()
    M = max(len(seq) for seq in Q.keys())
    for k in range(1,4):
        print "Explored Moves at step", k
        explored = (moves for moves in Q if len(moves) == k)
        for seq in explored:
            print seq, Q[seq]
        print




    # ##### Initialize #####
    # cummulativeQ = QMap()
    # gs = GameState(3)
    # gs.setPlayers(LearningPlayer('X', gs, 'reinforcement'), LearningPlayer('O', gs, 'reinforcement' ) )

    # ##### Play Games #####
    # n_games = 20
    # for game in range(n_games):
    #     gs.setQMap(cummulativeQ)     
    #     while not gs.game_finished:
    #         gs.takeStep()
    #         #print [k for k in gs.QMap.Q.keys() if len(k) == 1]
    #         gs.printGame()
    #     gs.printGame()
    #     print
    #     for p in gs.players:
    #         print p.mark, "is winner: ", p.is_winner
    #     cummulativeQ = gs.getQMap()
    #     gs.resetGame()
############# Tests ###################
    
    # # Debug game
    # cummulativeQ = QMap()    
    # gs = GameState(3)
    # gs.setQMap(QMap())
    # gs.setPlayers(LearningPlayer('X', gs, 'debug'), LearningPlayer('O', gs, 'ideal'))
    #problem_sequence =  [(1,'X'), (6, 'O'), (7,'X'), (4, 'O'), (8,'X'), (2, 'O'), (3, 'X'), (5, 'O'), (0, 'X')]   # problems with diag
    #problem_sequence = [(0,'X'),(7,'O'),(3,'X'),(6,'O'),(4,'X'),(8,'O'),(2,'X'),(1,'O'),(5,'X')] # problems horizontal tally
    #problem_sequence = [(4, 'X'), (0,'O'), (1,'X'), (6, 'O'), (3, 'X'), (5, 'O'), (7, 'X')]  # Optimize fail (X-random, O-minimize)
    #problem_sequence =  [(2, 'X'), (4, 'O'), (6, 'X'), (0, 'O'), (8, 'X'), (5, 'O'), (7, 'X')]# Corner powned
    #problem_sequence  =[(0, 'O'), (8, 'X'), (5, 'O'), (7, 'X')]  # Corner powned
    #problem_sequence = [(4,'X'), (0, 'O'), (5, 'X'), (3, 'O'), (8, 'X'), (2, 'O'), (1, 'X'), (7, 'O'), (6, 'X')] #blocking instead of winning
    #problem_sequence = [(5, 'X'), (4, 'O'), (8, 'X'), (2, 'O'), (6, 'X'), (1, 'O'), (7, 'X')] # not blocking

    # problem_sequence = [(4, 'X'), (0, 'O'), (8, 'X')] # Division by 0 error in indexInLine, diagonal fork
    # gs.players[0].setDebug(problem_sequence)
    # gs.setGameSequence(problem_sequence)
    # gs.setCurrentPlayer(gs.players[1])

    # problem_sequence = [(0, 'X'), (1, 'O'), (7, 'X'), (3, 'O'), (5, 'X')] # Division by 0 error belongsToLine
    # gs.players[0].setDebug(problem_sequence)    
    # gs.setGameSequence([(7, 'X'), (4, 'O')]) #list index out of range
    # gs.setCurrentPlayer(gs.players[0])
    # gs.players[0].setDebug([(8, 'X')])

    # problem_sequence = [(1, 'X'), (4, 'O'), (8, 'X'), (5, 'O'), (3, 'X'), (2, 'O'), (6, 'X'), (0, 'O'), (7, 'X')] # fork logic fail
    # gs.players[0].setDebug(problem_sequence)    
    
    #gs.setGameSequence([(2, 'X')])
    #gs.setCurrentPlayer(gs.players[1])

#    gs.players[0].setDebug(problem_sequence)
#    gs.players[1].setDebug(problem_sequence)

    # while not gs.game_finished:
    #     gs.takeStep()
    #     gs.printGame()
    # ################
    
    # # Find lines
    # s = GameState(5)
    # s.test_lines()
    
    # #Transform to 'standard' position
    # gs = GameState()
    # gs.testTransform() 
    
if __name__ == '__main__':
    run()
