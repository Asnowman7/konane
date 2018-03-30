# konane
Konane (Hawaiian Checkers) board game, command-line interface implementation

## Getting Started

After cloning the repository, run main.py in console to play a game of Konane against our AI :). The cpu's performance can be analyzed during the game by changing the global variable ANALYSIS_MODE in main.py to True.

## Implementation

### Board

The game board is a user defined class that initializes at the beginning of execution. The board itself is represented by an 8x8 2D list filled with one character strings. These strings represent the two players' pieces and blank spaces. The board class contains all methods that mutate the board and access information about the board. The __repr__ function prints the 2D list in console, one row per line.  

### Player

The players are objects of the user defined class, Player. Two players are initialized are at the beginning of execution - one human and one CPU. Each is assigned a piece type, either X or O, and each is assigned the other as an opponent. The player class contains methods that evaluate the board, generate all legal moves, and evaluate those moves using a minimax algorithm with optional alpha beta pruning.

#### AI

When the CPU wants to make a move, it calls the minimax helper function and specifies if it wants to use alpha-beta pruning or not. The minimax algorithms take in a board object, the last move taken to get that board state, the depth so far, and the depth bound. For alpha-beta pruning, alpha and beta values are also taken in as parameters. For analysis purposes, the number of evaluations made (and the number of cutoffs in alpha-beta pruning) is also tallied through the parameters.

To generate successor “nodes”, a new board object is made, and the next legal move is simulated on the new board. The new board, move made, incremented depth, alpha and beta values, and variables for analysis are then passed on in a recursive call. Creating a deep copy of the board is computationally expensive, and could be replaced if moves were saved in a stack and could be reversed.

## Analysis

Our analysis version of the project collects data pertaining to the number of cutoffs the minimax alph-bet pruning algorithm made, the number of move evaluations the cpu made, and the average branching factor of the minimax algorithm. After the cpu makes a move, the main execution prints the number of cutoffs, evaluations, and branching factor of the search for the move. 

There is an alternate main() function named exp_data_generator() that pits two cpu's against each other for 10 games at varying minimax depths, gleans the analysis data and times the execution of each minimax call, and appends the data to konane_analysis.csv.

## Authors

* **Austin Wan** - *Initial work* - [awan-23](https://github.com/awan-23)
* **Alex Snow** - *Initial work* - [Asnowman7](https://github.com/Asnowman7)

## Acknowledgments

* Special Thanks to Professor Deepak Kumar for organizing the project and teaching us the minimax algorithm. 