import sys
sys.path.append("../")

import pickle
import pandas as pd
from utilities import *

def run():
    ######################################################    
    #"lucky" Q-learning  vs Ideal and minimax TAble Stats

    size = 3
    with open("../Qs/lucky_3x3_Q.pickle", 'rb') as f:
        QM = pickle.load(f)      
        
    ratios = fightDuels([QM, QM, QM, QM, QM, QMap()],
                        [ ['ideal', 'Qlearning'  ],
                          ['Qlearning', 'ideal'  ],
                          ['minimax', 'Qlearning'],
                          ['Qlearning', 'minimax'],
                          ['Qlearning', 'Qlearning'],
                          ['random', 'random'    ]], size, n_games = 100 )
 
    cols = ["P1 win",  "draw", "P1 loss"]
    
    rows = ('ideal vs lucky_Q', 'lucky_Q vs ideal',
            'minimax vs lucky_Q', 'lucky_Q vs minimax',
            'lucky_Q vs lucky_Q','random vs random')
    
    table = pd.DataFrame(ratios, columns = cols, index = rows)
    print table
    # table.to_csv("../lucky_table.csv")
    print
    
    #################
    # lucky v Random
    randos = fightDuels([QM, QM, QM, QMap()], [ ['random', 'Qlearning'],
                                                ['Qlearning', 'random'],
                                                ['Qlearning', 'Qlearning'],
                                                ['random', 'random' ]  ], size, n_games = 1000, p1ds = [2,3,3,2], p2ds = [3,2,3,2] )
    cols = ["P1 win",  "draw", "P1 loss"]
    rows = ('random vs lucky_Q',
            'lucky_Q vs random',
            'lucky_Q vs lucky_Q',            
            'random vs random')
    table = pd.DataFrame(randos, columns = cols, index = rows)
    print table
    # table.to_csv("../lucky_random_table.csv")
    
    # # dd = pd.DataFrame(np.random.randn(10, 10)).applymap(abs)
    # # dd = dd.cumsum()
    # # print dd
    # # #plt.figure()
    # # dd.plot.bar(colormap='Greens')
    # # parallel_coordinates(data, 'Name', colormap='gist_rainbow')
    
if __name__ == "__main__":
    run()
