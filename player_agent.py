"""
This module contains all classes that consitute a player 
agent and its behaviour, i.e., a generic Player class, 
DecisionPlayer which inherits and expands upon Player,
and the QMap class

"""
# from game_state import GameState
# from strateegery import Strateegery

class Player(object):
    """
    A basic player class to form the basis of player agents.
    """
    mark = None
    
    def __init__(self, mark, game_state):
        self.game_state = game_state
        self.mark = mark
        self.is_winner = False
        
    def makeMove(self):
        pass

    
class QMap(object):
    """
    Contains the Q dictionary and methods for updating its keys
    and values.  
    """
   
    def __init__(self, gamma=0.1, alpha=0.1):
        self.Q = {}
        # Learning rates for Q learning
        self.gamma = gamma # For discounted sums
        self.alpha = alpha # For temporal difference
        
    def visitQ(self, sequence):
        # Add a new game sequence as a key to the dictionary initialized with value 0
        if not self.Q.get(sequence, False):
            self.Q[sequence] = 0

    # Q-learning update of the Q dictionary
    def updateQ(self, game, sgn, weight =1):
        
        n = len(game)
        alpha = self.alpha 
            
        reward = sgn#* weight**4 / n
            
        for i in range(1, len(game)):
            sub_sequence = tuple(game[:i])

            # Temporal-difference
            V = self.Q.get(sub_sequence, 0)
            X = sum([reward * self.gamma**(k-i) for k in range(i, len(game)) ]) #(n-i) * reward * self.gamma**(i-1)#
                
            self.Q[sub_sequence] = (1-alpha) * V + alpha * X
            
# End QMap 
###############################################################
            
class DecisionPlayer(Player):
    """
    This class defines a Player that can be instantiated with one
    of 7 decision strategies
      
    """
    
    def __init__(self, mark, game_state, policy, depth=2):
        super(DecisionPlayer, self).__init__(mark, game_state)
        self.policy = policy
        self.strategies  = Strateegery(self.game_state)
        self.depth = depth
        ##
        self.inner_Q = QMap()
        self.use_inner_Q = False
        
    def makeMove(self): 
        move = {
            'random'   : self.strategies.randomMove,
            'ideal'    : self.strategies.ideal,
            'minimax'  : self.strategies.minimaxMove,               
            'Qlearning': self.strategies.Qlearning,
            'miniQmax' : self.strategies.minimaxMove,

            'human'    : self.strategies.humanMove,
            'debug'    : self.debug}[self.policy]  # Player's policy dictates what function is called in strateegery
        
        if self.policy in ['minimax', 'miniQmax']:
            return move(self, self.depth)

        return move(self)
    
    def setInnerQ(self, QM): # For use by Qlearning instead of the global Q map
        self.use_inner_Q = True
        self.inner_Q = QM

    ########## Player for debugging ##########
    
    ## Load specific game sequences
    def setDebug(self, sequence):  
        from collections import deque
        self.inDebug = True
        self.problem_sequence = sequence
        self.Xmoves = deque([move for move in self.problem_sequence if move[1] == 'X'])
        self.Omoves = deque([move for move in self.problem_sequence if move[1] == 'O'])
        
    ## Call upon loaded sequences for replay
    def debug(self, player):
        self.strategies.ideal(self)
        if self.inDebug:
            if self.mark == 'X':
                return self.Xmoves.popleft()
            if self.mark == 'O':
                return self.Omoves.popleft()
        return

# End DecisionPlayer 
###############################################################
