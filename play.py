from random import randint
from game_board import GameBoard
from game_state import Player, GameState, QMap
from strateegery import Strateegery

class LearningPlayer(Player):
    def __init__(self, mark, game_state, policy):
        super(LearningPlayer, self).__init__(mark, game_state)
        self.policy = policy
        self.strategies  = Strateegery(self.game_state)
        
    def makeMove(self):
        gs = self.game_state
        
        move = {
            'random' : self.randomMove,
            'maximize' : None,
            'minimize' : None,
            'debug'    : self.debug}[self.policy]()

        #self.strategies.measureState()
        return move
    
    def randomMove(self):
        size = self.game_state.size
        valid = False
        move_index = None
        while not valid:
            move_index = randint(0, size**2 - 1)
            valid = self.game_state.validMove(move_index)
            
        return move_index, self.mark

    
    ########## Player for debugging ##########
    def setDebug(self, sequence):
        from collections import deque
        self.problem_sequence = sequence
        self.Xmoves = deque([move for move in self.problem_sequence if move[1] == 'X'])
        self.Omoves = deque([move for move in self.problem_sequence if move[1] == 'O'])
        
    def debug(self):
        if self.mark == 'X':
            return self.Xmoves.popleft()
        if self.mark == 'O':
            return self.Omoves.popleft()

        
def run():

    # ##### Initialize #####
    # cummulativeQ = QMap()
    # gs = GameState(3)
    # gs.setPlayers(LearningPlayer('X', gs, 'random') ,LearningPlayer('O', gs, 'random' ) )

    # ##### Play Games #####
    # n_games = 1
    # for game in range(n_games):
    #     gs.setQMap(cummulativeQ)     
    #     while not gs.game_finished:
    #         gs.takeStep()
    #         gs.printGrid(gs.makeGrid(gs.game_sequence))
    #         print "horizontals: ", gs.lines['Horizontal']
    #         print "verticals: ", gs.lines['Vertical']
    #         print "diagonals: ", gs.lines['Diagonal']
    #         print
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
    
    # # Update lines
    # s = GameState(5)
    # s.test_lines()

    # Reproduce buggy games
    cummulativeQ = QMap()    
    gs = GameState(3)
    gs.setQMap(QMap())
    gs.setPlayers(LearningPlayer('X', gs, 'debug'), LearningPlayer('O', gs, 'debug'))
    #problem_sequence =  [(1,'X'), (6, 'O'), (7,'X'), (4, 'O'), (8,'X'), (2, 'O'), (3, 'X'), (5, 'O'), (0, 'X')]   # problems with diag
    problem_sequence = [(0,'X'),(7,'O'),(3,'X'),(6,'O'),(4,'X'),(8,'O'),(2,'X'),(1,'O'),(5,'X')]
    gs.players[0].setDebug(problem_sequence)
    gs.players[1].setDebug(problem_sequence)

    while not gs.game_finished:
        gs.takeStep()
        gs.printGrid(gs.makeGrid(gs.game_sequence))
        print "horizontals: ", gs.lines['Horizontal']
        print "verticals: ", gs.lines['Vertical']
        print "diagonals: ", gs.lines['Diagonal']
        print
        
    # #Transform to 'standard' position
    # gs = GameState()
    # gs.testTransform()
    
    
if __name__ == '__main__':
    run()
