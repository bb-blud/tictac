import sys
sys.path.append("../")

import pickle
from time import time

from game_state import GameState
from player_agent import DecisionPlayer
from player_agent import QMap

from utilities import *

###################################################
# Final game strategy comparison miniQmax centric
###################################################

def run():
    size = 3
    with open("./newlucky.pickle") as f:
        luckyQ = pickle.load(f)

        
    def pipeTrain(pipeQ, size, lower, higher, itrs, depth=2):
        pipeQ, _, _ = playGames(setupGame(pipeQ, size, [lower, higher], learning=True,d1=depth-1, d2=depth), itrs[0])
        pipeQ, _, _ = playGames(setupGame(pipeQ, size, [higher,lower ], learning=True,d1=depth, d2=depth-1), itrs[1])
        pipeQ, _, _ = playGames(setupGame(pipeQ, size, [higher, higher],learning=True,d1=depth, d2=depth),   itrs[2])
        return pipeQ

    start = time()
    QM = QMap(gamma = 0.74, alpha=0.9)
    QM, tally, conv = playGames(setupGame(QM, size, ['random', 'random'],  learning=True), 1000)
    QM = pipeTrain(QM,size, 'random', 'Qlearning', [400, 400, 400])
    QM = pipeTrain(QM,size, 'Qlearning','miniQmax',[100, 100, 100], depth = 1)
    QM = pipeTrain(QM,size, 'Qlearning','miniQmax',[100, 100, 100], depth = 2)
    # #QM = pipeTrain(QM,size, 'Qlearning','miniQmax',[1000, 1000, 1000], depth = 3)

    print "training time" , time()-start

    exploreQ(QM, 3)
    duels = [['miniQmax', 'ideal' ],
             ['miniQmax', 'minimax'],
             ['miniQmax', 'Qlearning'],
             ['miniQmax', 'random'],
             
             ['random', 'random'],
             
             ['random', 'miniQmax'],
             ['Qlearning','miniQmax'],
             ['minimax', 'miniQmax'],
             ['ideal', 'miniQmax' ] ]
    
    # duels = [['Qlearning', 'ideal' ],
    #          ['Qlearning', 'minimax'],
    #          ['Qlearning', 'miniQmax'],
    #          ['Qlearning', 'random'],
             
    #          ['random', 'random'],
             
    #          ['random', 'Qlearning'],
    #          ['miniQmax','Qlearning'],
    #          ['minimax', 'Qlearning'],
    #          ['ideal', 'Qlearning' ] ]

    # with open("../pipeQ.pickle") as f:
    #     QM = pickle.load(f)

    start = time()
    ratios = []
    ## As Player 1
    ratios.append(getRatios(setupGame(QM, size, duels[0], d1=2              ), 100))
    ratios.append(getRatios(setupGame(QM, size, duels[1], d1=2, d2=2        ), 100))
    ratios.append(getRatios(setupGame(QM, size, duels[2], d1=2, p2QM=luckyQ ), 100))
    ratios.append(getRatios(setupGame(QM, size, duels[3], d1=2              ), 100))

    # Random
    ratios.append(getRatios(setupGame(QM, size, duels[4],                   ), 100))
    
    ## As player 2
    ratios.append(getRatios(setupGame(QM, size, duels[5], d2=2              ), 100))
    ratios.append(getRatios(setupGame(QM, size, duels[6], d2=2, p1QM=luckyQ ), 100))
    ratios.append(getRatios(setupGame(QM, size, duels[7], d1=2, d2=2        ), 100))
    ratios.append(getRatios(setupGame(QM, size, duels[8], d2=2              ), 100))

    print "total time: ", time() - start
    # with open("../pipeQ.pickle", 'wb') as f:
    #     pickle.dump(QM, f, pickle.HIGHEST_PROTOCOL)
        
    cols = ["P1 win",  "draw", "P1 loss"]
    rows = [r[0] +' v '+r[1] for r in duels]
    fintable = pd.DataFrame(ratios, columns = cols, index=rows)
    # fintable.to_csv('../pipeQ.csv')#"miniQmax_fin.csv')
    # fintable.plot.barh(colormap='Greens', stacked=True)
    plt.show()
    print fintable
    playGames(setupGame(luckyQ, 3, ['human', 'miniQmax'], d1=2), 2,check_convergence=False, debug=True)

if __name__ == "__main__":
    run()
