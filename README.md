# tictac

tictac is an exploration of Q-learning, a type of reinforcement learning, applied to the game of tictactoe.

## Documentation
A substantially detailed explanation of the ideas and motivation behind the code can be found right in this repository in
the form of a [pdf report](https://github.com/bb-blud/tictac/blob/master/report.pdf). There is also an accompanying 
IPython notebook that can be used to follow along when reading report.pdf (it is pretty tldr inducing, but whatevs, maybe for the curious).
## Usage
The state of the code at this moment unfortunately is pretty user unfriendly :(  
However by downloading the files and running;  
`python2.7 play.py`   
in your shell, a Q-learning based 3x3 model will be trained and you will be able to play against it (rather crudely)  
by specifying the index of your next move on the grid. Indices ranging from 0 to 9. It is not super smart, it can spot some  
forks, blind to others. The codebase however is designed for arbitrary sized nxn tictactoe, though training becomes very
resource consuming for anything above n = 4.  
## More Info
Two different "Perfect" or near perfect players are also implemented and can be played against, but again at this point only  
if one digs through the code. Of the two, "ideal", is pretty usable for n = 17 or so.
## License
License can be found [here](https://github.com/bb-blud/tictac/blob/master/license.txt)
