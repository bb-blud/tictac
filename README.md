# tictac

tictac is an exploration of Q-learning, a type of reinforcement learning, applied to the game of tictactoe.

## Documentation
A substantially detailed explanation of the ideas and motivation behind the code can be found right in this repository in
the form of a [pdf report](https://github.com/bb-blud/tictac/blob/master/report.pdf) (It can be a pretty tedious read, but for the curious).
## Usage
tictac now sports a Kivy based gui were you can select a game size and strategies for the two players. As of this update to README
I haven't yet included human player input, though one can pit and observe the different playing agent strategies.
Simply by downloading the files and running;  
`python2.7 play.py`   
in your shell, will fire up the gui. 
## More Info
There are two different Q-learning based "brains" that have already been trained for 3x3 gameplay. Of the two miniQmax was the most successful. It is reasonably smart, it can spot some forks, blind to others. The codebase however is designed for arbitrary sized nxn tictactoe, though training becomes very resource consuming for anything above n = 4. Two different "Perfect" or near perfect players are also implemented and can be played against.  Of the two, "ideal", is pretty usable for up to n = 17 or so. The other, is basically an implementation of minimax with alpha-beta pruning applied to tictactoe, which is slow for anything above n=5. Ideal and minimax are hardcoded algorithms and did not involve any type of machine learning. I used them as benchmarks basically as I explored the reinforcement learning problem.

## Somewhat cool?
I will also include a train-miniQmax strategy that will let the user play against and train a Q for gamesizes between 3 and 9. Even the perfect players can be used to train it. This was something I explicitly avoided during the project as I wanted minQmax to learn only from its own gameplay.

## For some later time
Since put simply, playing tictactoe doesn't really make it to the top tens of awesome things to do with one's time, I want to eventually modify the game so that the size of the board does not equal to the amount of marks in a row required for a win. So you could play for three marks in a row on a 5x5 board for example. I feel this might be somewhat interesting and entertaining for a human, as it would be more like a gaining territory game. That's it for now!

## License
License can be found [here](https://github.com/bb-blud/tictac/blob/master/license.txt)
