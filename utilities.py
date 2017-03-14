"""
This module houses utility functions used to train agents, 
play multiple games, graph statistics, as well as some diagnostic
printout functions.

"""

def setupGame(globalQM, game_size, policies, learning=False, marks=['X','O'], p1QM=None, p2QM=None, d1=2, d2=2):
    """
    Set up all parameters for a game to be played. Returns a GameState instance

    """
    gs = GameState(game_size,  learning)
    gs.setQMap(globalQM)
    
    player1 = DecisionPlayer(marks[0], gs, policies[0], d1)
    if p1QM is not None:
        player1.setInnerQ(p1QM)

    player2 = DecisionPlayer(marks[1], gs, policies[1], d2)
    if p2QM is not None:
        player2.setInnerQ(p2QM)

    gs.setPlayers(player1, player2)

    return gs

def getRatios(game_state, n_games, debug=False):
    """
    Play games and return totals for win:draw:loss divided by total games

    """
    QM, tally, conv = playGames(game_state, n_games, debug=debug)
    
    ts = [1.*tally[(True, False)], 1.*tally[(False, True)], 1.*tally[(False,False)]]
    
    s = sum(ts)
    return [ts[0]/s, ts[2]/s, ts[1]/s]

def fightDuels(QMs, duels, size, n_games, **kwargs):
    """
    Convenience method multiple duels can be played and an array of final ratio arrays is returned

    """
    ratios = []

    p1depths = kwargs.get('p1ds', [2 for _ in range(len(duels))]) # get the depths for each game or set all to 2 if
    p2depths = kwargs.get('p2ds', [2 for _ in range(len(duels))]) # depths are not specified.
        
    for i, duel in enumerate(duels):
        ratios.append(getRatios(setupGame(QMs[i], size, duel, d1 = p1depths[i], d2 = p2depths[i] ),  n_games) )
        
    return ratios

def playGames(game_state, n_games, check_convergence=True,  debug=False):
    """
    This function will play n_game amount of games iteratively and by
    default check for game convergence, in which case it will exit early
    so as to stop playing the same game repeatedly.

    """

    ####### Tally ########
    tally = { (True, False) : 0, (False, True) : 0, (False, False) : 0 }
    is_converging = False
    
    ##### Initialize #####
    gs = game_state
    
    #### Crude convergence test ####
    repeats = deque()                   #
    if check_convergence:               # A buffer of the last 10 games played is created
        buffer_size = 10
        # if gs.learning:
        #     buffer_size = 3*n_games
        for game in range(buffer_size): #
            while not gs.game_finished: # Filling buffer
                gs.takeStep()
                if debug:
                    gs.printGame()
            repeats.append(gs.game_sequence)
            gs.resetGame()

    ######### Play Games #########
    current = []                 #
    for game in range(n_games):  # Main game playing loop 

        while not gs.game_finished:
            gs.takeStep()
            if debug:
                gs.printGame()
        if debug:
            gs.printGame()
            print

        tally[ (gs.players[0].is_winner, gs.players[1].is_winner) ] += 1 ##Update game tally

        if debug:
            for p in gs.players:
                print p.mark, "is winner: ", p.is_winner
            print tally

        ## Exit if converging ##
        current = gs.game_sequence
        repeats.append(current) #Append the last game played to buffer
        repeats.popleft()       #remove the last game from the buffer

        if debug:
            for r in repeats:
                print r
                print "**"
            print
            
        # If all games in the repeats buffer are equal then players have converged to a single game 
        if False not in (current == g for g in repeats) and check_convergence: 
            print "CONVERGENCE ON GAME NUMBER: ", game, [p.policy for p in gs.players]
            is_converging = True
            break
        ## ##  ## ##
        
        gs.resetGame()

    
    return gs.QM, tally, is_converging

def multiTrain(game_state, runs, batch_size):
    
    ## Support function plays batch_size amount of games ##
    def playBatch(ns, game_state, batch_size):
        gs = game_state
        for game in range(batch_size):
            gs.QM = ns.QM
            while not gs.game_finished:
                gs.takeStep()
            ns.QM = gs.QM
            gs.resetGame()
    ##   ##   ##   ##    ##   ##   ##   ##  
   
    import multiprocessing
    manager = multiprocessing.Manager()
    ns = manager.Namespace()
    ns.QM = game_state.QM
    #ns.Q = game_state.QM.Q
    
    jobs = []
    for _ in range(runs):
        p = multiprocessing.Process(target=playBatch, args=(ns, game_state, batch_size) )
        jobs.append(p)
        p.start()
        
    for p in jobs:
        p.join()

    return ns.QM

def graphStats(columns, data, strategy): #Based on http://matplotlib.org/examples/pylab_examples/table_demo.html
    rows = ['win', 'draw', 'loss']
    values = np.arange(0, 1, .1)
    value_increment = 2

    # Get some pastel shades for the colors
    colors = plt.cm.BuPu(np.linspace(0, 0.5, len(rows)))[::-1]
    n_rows = len(data)

    index = np.arange(len(columns)) + 0.3
    bar_width = 0.4

    # Initialize the vertical-offset for the stacked bar chart.
    y_offset = np.array([0.0] * len(columns))

    # Plot bars and create text labels for the table
    cell_text = []
    for row in range(n_rows):
        plt.bar(index, data[row], bar_width, bottom=y_offset, color=colors[row])
        y_offset = y_offset + data[row]
        cell_text.append(['%.4f' % x for x in data[row]])

    # Add a table at the bottom of the axes
    the_table = plt.table(cellText=cell_text,
                          rowLabels=rows,
                          rowColours=colors,
                          colLabels=columns,
                          loc='bottom')

    # Adjust layout to make room for the table:
    plt.subplots_adjust(left=0.2, bottom=0.2)

    plt.ylabel("win/draw/loss fraction".format(value_increment))
    plt.yticks(values * value_increment, ['%.2f' % (val*value_increment) for val in values])
    plt.xticks([])
    plt.title('Ratio Comparison ' + strategy)

    plt.show()

def printTally(game_state, n_games):
    
    QM, tally, conv = playGames(game_state, n_games)
    
    ts = [1.*tally[(True, False)], 1.*tally[(False, True)], 1.*tally[(False,False)]]
    
    s = sum(ts)
    print "{} : {} : {}".format(ts[1]/s, ts[2]/s, ts[0]/s)


def exploreQ(QM,d):
    Q = QM.Q
    M = max(len(seq) for seq in Q.keys())
    for k in range(1,M/d):
        print "Explored Moves at step", k
        explored = sorted( [(seq , Q[seq]) for seq in Q if len(seq) == k], key=lambda t:t[1] )
        
        for seq, val  in explored:
            print seq, val
        print
