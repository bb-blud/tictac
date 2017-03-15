import sys
sys.path.append("../")

import pickle
from utilities import *

def run():
    
    ####################################################
    # "lucky" Q-learning  vs Ideal and minimax GRaphs
    
    size = 3
    with open("../Qs/lucky_3x3_Q.pickle", 'rb') as f:
        QM = pickle.load(f)
        
    #QM, tally, conv = playGames(setupGame(QM, size, ['Qlearning','minimax']), 1)
        
    #############################
    # Q-learning vs Ideal stats 
    columns  = ('Ideal vs lucky_Q', 'lucky_Q vs Ideal', 'random vs Ideal', 'Ideal vs random')
    
    ratios = fightDuels([QM, QM, QMap(), QMap()], [ ['ideal', 'Qlearning'],
                                                    ['Qlearning', 'ideal'],
                                                    ['random', 'ideal'   ],
                                                    ['ideal', 'random' ] ], size, n_games = 100, p1ds = [2,3,2,2], p2ds = [3,2,2,2] )
    
    ratios = np.transpose(ratios)

    graphStats(columns, ratios, 'lucky-Q vs Ideal {}x{}'.format(size,size))

    ################################
    # Q-learnin vs Minimax stats 
    columns  = ('Minimax vs lucky_Q', 'lucky_Q vs Minimax', 'random vs Minimax', 'Minimax vs random')
    
    ratios = fightDuels([QM, QM, QMap(), QMap()],[ ['minimax', 'Qlearning'],
                                                   ['Qlearning', 'minimax'],
                                                   ['random', 'minimax'],
                                                   ['minimax', 'random']  ], size, n_games = 20, p1ds = [2,3,2,2], p2ds = [3,2,2,2] )
    ratios = np.transpose(ratios)

    graphStats(columns, ratios, 'lucky-Q vs Minimax {}x{}'.format(size,size))

    ################################
    # Q-learn vs Random stats 
    columns  = ('Random vs Qlearning',  'Qlearning vs Random', 'Random vs Random', '"Perfect" random')
    
    duels = fightDuels([QM, QMap(), QMap()], [ ['random', 'Qlearning'],
                                               ['Qlearning', 'random'],
                                               ['random', 'random' ]  ], size, n_games = 100, p1ds = [2,3,2], p2ds = [3,2,2] )
    duels.append([91.0/138, 3.0/138, 44.0/138 ])
    ratios = np.transpose(duels)
    
    graphStats(columns, ratios, 'lucky-Q/Random Comparison {}x{}'.format(size,size))

if __name__ == "__main__":
    run()
