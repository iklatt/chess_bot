# File Summaries
## chess_evaluation.py:
This is the file that contains the functions used for evaluating a given chess board.  Currently uses two helper functions.  One function associates values to each piece on the chess board, e.g. a knight is worth 100.  The other helper function uses piece position tables to give points for pieces being on good squares, e.g. knights are given more value when they are centralized since they are much more useful in the center than on the edge.  All function take in a coefficient list, which is used to tweak the values of given aspects of the evaluation.  For example, the knight is currently worth 300, but we later decide that the knight should only be worth 150, then we would change its coefficient to 0.5.  The reason these coefficients exist can is due to [this part](#tweaking-evaluation-function) of my future plans.

## chess_bot_search.py
This is the file where all search related functions are.  The current search functionality is standard alpha beta pruning with iterative deepening.

## play_against_bot.py
This is the file that is run when you want to play against the AI.  It is currently quite bare-bones, but I have plans to update it which can be found [here](#ui).

# Future Plans

## UI
The biggest feature I want to add is a more friendly UI.  Currently moves have to be typed into the terminal and the board is simply printed to the terminal, which is not ideal.  I want to make a more standard UI board, i.e. the board is an image and the user can drag and drop the pieces to make their moves. 

## Search Optimization
One of the main things I need to focus on is optimization of the search algorithm. One method I plan to implement in the future is to store previously checked positions in a transposition table in the form of a 64 bit number via Zobrist Hashing.  This should be faster since the search function won't have to check the same position multiple times.  Another method I want to use to improve speed is called move ordering.  Since we are using alpha beta pruning, we want to check the best moves first since that will result in much more pruning.

## Tweaking Evaluation Function
After optimizing the search function I want to make use of the ideas used in [this paper](https://arxiv.org/pdf/1711.08337.pdf) to improve my evaluation function. To summarize the paper, the authors used an evaluation function that takes in 35 different parameters which act as weights for the given aspects of board evaluation.  For example, part of their evaluation function takes into account the mobility of the queen and this value is then weighted more or less to change how the bot will evaluate the position, more favoring positions with high queen mobility and less the opposite.  They then took a large amount of decisive games, that is no games that ended in a draw, from high level chess players and randomly select some positions with the winning player to move.  The genetic algorithm is used, where the fitness if a given individual is the number of times that it chose the same move that the winning player did in the random position.  This allows them to tackle the evaluation problem by trying to simulate high rated players.  They also use the genetic algorithm to prune searches.  They did this by collecting a large amount of chess puzzles, that is positions with a "best" move, with the fitness of the individuals being how many moves it considered before finding the correct move, where less moves is better.  They ran the evolution process for position evaluation 10 times and used the genetic algorithm once again, with the fittest individual from each of the 10 evolutionary processes being used as the initial population.  They had the individuals play against each other, ranked them, and chose the fittest individuals based off those rankings.  

## Openings
One other thing I would like to change is add an opening book.  Most modern chess engines just use an opening book for their first moves.  One way I might do this is simply store the openings of a few games, maybe 1000 or so, and simply play the move played in those games.  When there is a move played that deviates from those games the engine will simply use its normal method of choosing moves. 
