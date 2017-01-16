from time import time
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
            'Qlearning': self.strategies.Qlearning,
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


def playGames(cummulativeQ, game_state, policies, n_games, to_convergence=False, debug=False):
    ####### Tally ########
    tally = { (True, False) : 0, (False, True) : 0, (False, False) : 0 }

    ##### Initialize #####
    gs = game_state
    gs.setPlayers(LearningPlayer('X', gs, policies[0]), LearningPlayer('O', gs, policies[1] ) )

    #### Crude convergence test ####
    from collections import deque
    
    repeats = deque()
    for game in range(5):
        gs.setQMap(cummulativeQ)
        while not gs.game_finished:
            gs.takeStep()
            if debug:
                gs.printGame()
        repeats.append(gs.game_sequence)
        cummulativeQ = gs.QMap
        gs.resetGame()

    ######### Play Games #########
    bads = set() # debug
    
    current = []
    converged = False
    while not converged:                            # Default, avoid seeking convergence
        converged = not to_convergence or converged # Change default behaviour to seek convergence (If-then logic)
        for game in range(n_games):
            gs.setQMap(cummulativeQ)

            while not gs.game_finished:
                gs.takeStep()
                if debug:
                    gs.printGame()
            if debug:
                gs.printGame()
                print

            cummulativeQ = gs.QMap
            tally[ (gs.players[0].is_winner, gs.players[1].is_winner) ] += 1

            if debug:
                for p in gs.players:
                    print p.mark, "is winner: ", p.is_winner
                print tally

            ## Exit if converging ##
            current = gs.game_sequence
            repeats.append(gs.game_sequence)
            repeats.popleft()

            if debug:
                for r in repeats:
                    print r
                    print "**"
                print
            
            if False not in (current == g for g in repeats):
                tally[ (False, False) ] -= 4
                if True:
                    print "CONVERGENCE ON GAME NUMBER: ", game
                converged = True
                break
            ## ##  ## ##

            # if debug:
            #     if gs.players[0].is_winner:
            #         bads.add(tuple(gs.game_sequence))

            gs.resetGame()
        
        # for b in bads:
        #     print b
    
    return cummulativeQ, tally


    
def trainQ(QM, game_state, policies, runs, batch_size):

    ## Support function plays batch_size amount of games ##
    def playBatch(ns, game_state, policies, batch_size):
        gs = game_state
        gs.setPlayers(LearningPlayer('X', gs, policies[0]), LearningPlayer('O', gs, policies[1]) )

        for game in range(batch_size):
            gs.setQMap(ns.QM)
        
            while not gs.game_finished:
                gs.takeStep()
            ns.QM = gs.QMap
            gs.resetGame()     
    ##   ##   ##   ##    ##   ##   ##   ##  
   
    import multiprocessing
    manager = multiprocessing.Manager()
    ns = manager.Namespace()
    ns.QM = QM
    
    jobs = []
    for _ in range(runs):
        p = multiprocessing.Process(target=playBatch, args=(ns, game_state, policies, batch_size) )
        jobs.append(p)
        p.start()
        
    for p in jobs:
        p.join()

    return ns.QM


def printTally(q_map, game_state, playerX, playerO, n_games):
    
    QM, tally = playGames(q_map, game_state, [playerX, playerO], n_games)
    
    ts = [1.*tally[(True, False)], 1.*tally[(False, True)], 1.*tally[(False,False)]]
    
    s = sum(ts)
    print "{} : {} : {}".format(ts[0]/s, ts[2]/s, ts[1]/s)
        
def run():
    size = 4
    # start = time()
    # QM, tally = playGames(QMap(), GameState(size, learning=True), ['Qlearning', 'Qlearning'], 100, to_convergence=True)
    # print "Time elapsed: {} ".format(time() - start)
    # print tally

    ######################
    # Minimax rough stats
    # print "Minimax rough stats {}x{}".format(size,size)
    # print "Perfect X player win/draw/loss ratio 91:3:0"
    # print "Perfect Normalized" 
    # print "0.9681 : 0.0319 : 0"
    # print "Minimax vs Random"
    # start = time()
    # printTally(QMap(), GameState(size), 'minimax', 'random', 500)
    # print "Time elapsed: {} ".format(time() - start)
    # print
    # print "Perfect O player loss/draw/win ratio 0:3:44"
    # print "Perfect Normalized"
    # print  "0 : 0.0638 : 0.9363"
    # print "Random vs Minimax"
    # start = time()
    # printTally(QMap(),GameState(size), 'random', 'minimax',500)
    # print "Time elapsed: {} ".format(time() - start)

    # print
    
    # ######################
    # # Ideal rough stats
    # print "Ideal rough stats {}x{}".format(size,size)
    # print "Perfect X player: win/draw/loss ratio 91:3:0"
    # print "Perfect Normalized:"
    # print "0.9681 : 0.0319 : 0"
    # print "Ideal vs Random"
    # start = time()
    # printTally(QMap(), GameState(size), 'ideal', 'random', 1000)
    # print "Time elapsed: {} ".format(time() - start)
    # print
    # print "Perfect O player loss/draw/win ratio 0:3:44"
    # print "Perfect Normalized:"
    # print "0 : 0.0638 : 0.9363"
    # print "Random vs Ideal"
    # start = time()
    # printTally(QMap(), GameState(size), 'random', 'ideal', 1000)
    # print "Time elapsed: {} ".format(time() - start)

    # print
    
    # ######################
    # # Random rough stats
    # print "Random rough stats {}x{}".format(size,size)
    # print "TicTacToe X-O win/loss/draw ratio: 91:44:3"
    # print "Normalized:"
    # print "0.6594 : 0.31884 : 0.0217"
   
    print "Random vs Random\nBoard {}x{}".format(size,size)
    start = time()
    printTally(QMap(),GameState(size), 'random', 'random', 100)
    print "Time elapsed: {} ".format(time() - start)
    print

    print

    ############################
    # Q-Learning rough stats
    
    # # Seed Q with initial random games
    # QM, tally = playGames(QMap(), GameState(size, learning=True), ['random', 'random'], 70)
    # # player 2 learning against a random player 1
    # QM, tally = playGames(QM, GameState(size, learning=True), ['random', 'Qlearning'], 1000, to_convergence=False)
    # # Now player 1 learning against a random player 2
    # QM, tally = playGames(QM, GameState(size, learning=True), ['Qlearning', 'random'], 1000, to_convergence=False)
    # Have two agents learn against each other
    # QM, tally = playGames(QM, GameState(size, learning=True), ['Qlearning', 'Qlearning'])


    # Seed Q with initial random games
    start = time()
    QM = trainQ(QMap(), GameState(size, learning=True), ['random', 'random'], runs=7, batch_size=100)
    # player 2 learning against a random player 1
    QM = trainQ(QM, GameState(size, learning=True), ['random', 'Qlearning'], runs=10, batch_size=100)
    # Now player 1 learning against a random player 2
    QM = trainQ(QM, GameState(size, learning=True), ['Qlearning', 'random'], runs=10, batch_size=100)
    # Have two agents learn against each other
    # QM = trainQ(QM, GameState(size, learning=True), ['Qlearning', 'Qlearning'], runs=10, batch_size=300)
    print time() - start
    print "seeking converge"
    QM, tally = playGames(QM, GameState(size, learning=True), ['Qlearning', 'Qlearning'], 100,to_convergence=True)
    print time() - start
    
    # print "Q-Learning rough stats {}x{}".format(size,size)
    # print "TicTacToe X-O win/loss/draw ratio: 91:44:3"
    # print "Normalized:"
    # print "0.6594 : 0.31884 : 0.0217"
    # print "Qlearning vs random\nBoard {}x{}".format(size,size)
    # printTally(QM, GameState(size), 'random', 'random', 1000)
    # print

    # print "TicTacToe X-O win/loss/draw ratio: 91:44:3"
    # print "Normalized:"
    # print "0.6594 : 0.31884 : 0.0217"
    # print "random vs Qlearning\nBoard {}x{}".format(size,size)
    # printTally(QM, GameState(size), 'random', 'random', 1000)
    # print
    
    QM, tally = playGames(QM, GameState(size), ['Qlearning', 'ideal'], 30)
    print tally

    QM, tally = playGames(QM, GameState(size), ['Qlearning', 'minimax'], 30)
    print tally

    QM, tally = playGames(QM, GameState(size), ['Qlearning', 'Qlearning'], 30)
    print tally

    ##### Explore Q #####
    # Q = QM.getQ()
    # M = max(len(seq) for seq in Q.keys())
    # for k in range(1,M):
    #     print "Explored Moves at step", k
    #     explored = (moves for moves in Q if len(moves) == k)
    #     for seq in explored:
    #         print seq, Q[seq]
    #     print

    ####### Store/Load QMap #########
    # import pickle
    # with open("./lucky_4x4_Q.pickle", 'wb') as f:
    #     pickle.dump(QM, f, pickle.HIGHEST_PROTOCOL)
    # with open("./lucky_3x3_Q.pickle", 'rb') as f:
    #     QM = pickle.load(f)
        



############## Tests ###################
    
    # # Debug game
    # cummulativeQ = QMap()    
    # gs = GameState(3)
    # gs.setQMap(QMap())
    # gs.setPlayers(LearningPlayer('X', gs, 'debug'), LearningPlayer('O', gs, 'minimax')) 
    # problem_sequence =  [(1,'X'), (6, 'O'), (7,'X'), (4, 'O'), (8,'X'), (2, 'O'), (3, 'X'), (5, 'O'), (0, 'X')]   # problems with diag
    # problem_sequence = [(0,'X'),(7,'O'),(3,'X'),(6,'O'),(4,'X'),(8,'O'),(2,'X'),(1,'O'),(5,'X')] # problems horizontal tally
    # problem_sequence = [(4, 'X'), (0,'O'), (1,'X'), (6, 'O'), (3, 'X'), (5, 'O'), (7, 'X')]  # Optimize fail (X-random, O-minimize)
    # problem_sequence =  [(2, 'X'), (4, 'O'), (6, 'X'), (0, 'O'), (8, 'X'), (5, 'O'), (7, 'X')]# Corner powned
    # problem_sequence  =[(0, 'O'), (8, 'X'), (5, 'O'), (7, 'X')]  # Corner powned
    # problem_sequence = [(4,'X'), (0, 'O'), (5, 'X'), (3, 'O'), (8, 'X'), (2, 'O'), (1, 'X'), (7, 'O'), (6, 'X')] #blocking instead of winning
    # problem_sequence = [(5, 'X'), (4, 'O'), (8, 'X'), (2, 'O'), (6, 'X'), (1, 'O'), (7, 'X')] # not blocking
    # problem_sequence = [(4, 'X'), (0, 'O'), (8, 'X')] # Division by 0 error in indexInLine, diagonal fork
    # problem_sequence = [(0, 'X'), (1, 'O'), (7, 'X'), (3, 'O'), (5, 'X')] # Division by 0 error belongsToLine    
    # problem_sequence = [(1, 'X'), (4, 'O'), (8, 'X'), (5, 'O'), (3, 'X'), (2, 'O'), (6, 'X'), (0, 'O'), (7, 'X')] # fork logic fail
    # problem_sequence = [(7, 'X'), (4, 'O'), (3, 'X'), (2, 'O'), (6, 'X'), (0, 'O'), (8, 'X')] # fork fail
    # problem_sequence = [(0, 'X'), (4, 'O'), (5, 'X'), (6, 'O'), (2, 'X'), (1, 'O'), (8, 'X')] # minimax fail to see fork
    # gs.players[0].setDebug(problem_sequence)

    # while not gs.game_finished:
    #     gs.takeStep()
    #     gs.printGame()
    # gs.printGame()
    ################

    
    # problem_sequence = [(4, 'X'), (0, 'O'), (8, 'X')] # Division by 0 error in indexInLine, diagonal fork
    # gs.players[0].setDebug(problem_sequence)
    # gs.setGameSequence(problem_sequence)
    # gs.setCurrentPlayer(gs.players[1])

    # problem_sequence = [(0, 'X'), (1, 'O'), (7, 'X'), (3, 'O'), (5, 'X')] # Division by 0 error belongsToLine
    # gs.players[0].setDebug(problem_sequence)    
    # gs.setGameSequence([(7, 'X'), (4, 'O')]) #list index out of range
    # gs.setCurrentPlayer(gs.players[0])
    # gs.players[0].setDebug([(8, 'X')])


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














    
    # ##### Initialize #####
    # cummulativeQ = QMap()
    # gs = GameState(3)
    # gs.setPlayers(LearningPlayer('X', gs, 'Qlearning'), LearningPlayer('O', gs, 'Qlearning' ) )

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
    

