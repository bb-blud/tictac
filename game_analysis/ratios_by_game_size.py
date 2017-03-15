import sys
sys.path.append("../")

from utilities import *

def run():
    # Approximate baseline win/draw/loss ratios using random policy
    size = 3
    columns  = ('"Perfect" Random', 'random vs random')
    
    # TicTacToe X-O win/loss/draw ratio: 91:44:3 or 0.6594 : 0.31884 : 0.0217, source wikipedia
    ratios = [[91.0/138, 3.0/138, 44.0/138 ]]
    ratios += fightDuels([QMap()], [['random', 'random']], size, n_games = 10000)

    ratios = np.transpose(ratios)
    graphStats(columns, ratios, 'random 3x3')

    ##
    size = 4
    columns = ('Trial 1', 'Trial 2')
    ratios = np.transpose(fightDuels([QMap(), QMap()], [ ['random','random'], ['random','random'] ], size, 10000))

    graphStats(columns, ratios, 'Approximate baseline win/draw/loss ratios 4x4')

    ## 
    size = 5
    columns = ('Trial 1', 'Trial 2')
    ratios = np.transpose(fightDuels([QMap(), QMap()], [ ['random','random'], ['random','random'] ], size, 10000))

    graphStats(columns, ratios, 'Approximate baseline win/draw/loss ratios 5x5')

    ##
    size = 6
    columns = ('Trial 1', 'Trial 2')
    ratios = np.transpose(fightDuels([QMap(), QMap()], [ ['random','random'], ['random','random'] ], size, 10000))

    graphStats(columns, ratios, 'Approximate baseline win/draw/loss ratios 6x6')

if __name__ == "__main__":
    run()
