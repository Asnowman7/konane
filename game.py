"""
konane game file
Austin Wan & Alex Snow
"""
import pdb
from copy import deepcopy

O_PIECE = "O"
X_PIECE = "X"
BLANK_SPACE = "."
MOVE_DICT = {"E":(0, 1), "W":(0, -1), "S":(1, 0), "N":(-1, 0)}
INFINITY = float("inf")
NEG_INF = float("-inf")
DEPTH_BOUND = 4

class Board:

    def __init__(self, size):
        """Initialize a board object
        :param int size: length and width of board
        """
        self.size = size
        self.num_x_piece = 0
        self.num_o_piece = 0
        self.matrix = [[0 for col in range(size)] for row in range(size)]
        self.prev_matrix = []
        self.preprev_matrix = []
        self.num_x_edges = size*4 - 4
        self.num_o_edges = size*4 - 4
        for i in range(size):
            for j in range(size):
                if i % 2 == 0:
                    if j % 2 == 0:
                        self.matrix[i][j] = X_PIECE
                        self.num_x_piece += 1
                    else:
                        self.matrix[i][j] = O_PIECE
                        self.num_o_piece += 1
                else:
                    if j % 2 == 0:
                        self.matrix[i][j] = O_PIECE
                        self.num_o_piece += 1
                    else:
                        self.matrix[i][j] = X_PIECE
                        self.num_x_piece += 1


    def __repr__(self):
        str_mat = " "
        for i in range(self.size):
            str_mat += "   " + str(i + 1)
        str_mat += "\n"
        for i in range(self.size):
            str_mat += str((i + 1))
            for piece in self.matrix[i]:
                    str_mat += "   " + piece
            str_mat += "\n"
        return str_mat

    def get_space(self, coords):
        """Get the type of the piece in a given space
        :param tuple coords: The coordinates of the space to be checked
        :return: string character describing type of piece in the space
        """
        # coords is a (row, col) tuple
        return self.matrix[coords[0]][coords[1]]

    def get_num_pieces(self, piece_type):
        """Get the number of pieces of piece_type still on the board
        :param str piece_type: The piece type to be counted
        :return: int number of pieces of the given piece still on the board
        """
        if piece_type == X_PIECE:
            return self.num_x_piece
        else:
            return self.num_o_piece

    def on_board(self, coords):
        """Check if the coordinates given are part of the board
        :param tuple coords: coordinates of space in question
        :return: boolean
        """
        # coords is [row, col] of the space in question
        return (coords[0] >= 0 and coords[0] < self.size) and \
               (coords[1] >= 0 and coords[1] < self.size)

    def change_space(self, coords, piece):
        """Change the space to a given piece_type, and also updates
        numbers of x and o pieces.
        :param tuple coords: coordinates of the space to be changed
        :param str piece: the piece_type to be changed to
        """
        orig_piece = self.get_space(coords)
        edge = [0, self.size-1]
        on_edge = coords[0] in edge or coords[1] in edge
        if orig_piece == X_PIECE:
            self.num_x_piece -= 1
            if on_edge:
                self.num_x_edges -= 1
        elif orig_piece == O_PIECE:
            self.num_o_piece -= 1
            if on_edge:
                self.num_o_edges -= 1
        if piece == X_PIECE:
            self.num_x_piece += 1
            if on_edge:
                self.num_x_edges += 1
        elif piece == O_PIECE:
            self.num_o_piece += 1
            if on_edge:
                self.num_o_edges += 1
        self.matrix[coords[0]][coords[1]] = piece


    def make_move(self, move):
        """Saves previous board as the prevprev board, saves the current board
        as the previous board, and makes move by changing pieces on board.
        :param Move move: Move object with from-coordinates and to-coordinates
        Move is assumed to be legal.
        """
        self.preprev_matrix = deepcopy(self.prev_matrix)
        self.prev_matrix = deepcopy(self.matrix)  # in case undo is needed
        moving_piece = self.get_space(move.from_coords)
        direc = move.direc
        dist = abs((move.from_coords[0] - move.to_coords[0]) +
                   (move.from_coords[1] - move.to_coords[1]))
        curr_space = move.from_coords
        for i in range(dist):
            self.change_space(curr_space, BLANK_SPACE) # noms
            curr_space = (curr_space[0] + MOVE_DICT[direc][0],
                          curr_space[1] + MOVE_DICT[direc][1])
        self.change_space(move.to_coords, moving_piece)

    def undo_move(self):
        """Undoes last round of moves (player & cpu move).
        Note: Can only be called once a turn.
        """
        self.matrix = self.preprev_matrix


class Move:

    def __init__(self, from_coords, to_coords, direc):
        """Initializes Move class object.
        :param tuple from_coords: contains coordinates of piece to be moved
        :param tuple to_coords: contains coordinates of destination space
        :param str direc: either S, W, N, or E indicating direction of travel
        """
        self.from_coords = from_coords
        self.to_coords = to_coords
        self.direc = direc

    def __repr__(self):
        from_row, from_col = self.from_coords[0:2]
        to_row, to_col = self.to_coords[0:2]
        return "((" + str(from_row + 1) + ", " + str(from_col + 1) + "), (" +\
        str(to_row + 1) + ", " + str(to_col + 1) + "), " + self.direc + ")"

    def compare_move(self, other_move):
        """Checks if Move object is identical to other_move.
        :param Move other_move: move object to be compared against
        :return: boolean
        """
        return (self.from_coords == other_move.from_coords) and\
         (self.to_coords == other_move.to_coords) and\
         (self.direc == other_move.direc)


class Player:

    def __init__(self, human, piece_type):
        """Initialize Player object.
        :param bool human: is player object controlled by human
        :param str piece_type: either 'O' or 'X'
        """
        self.human = human
        self.piece_type = piece_type
        if piece_type == X_PIECE:
                self.opponent_type = O_PIECE
        else:
                self.opponent_type = X_PIECE

        self.opponent = None

    def assign_opponent(self, opponent):
        """Assigns opponent player object to class attribute.
        :param Player opponent: the opponent player object
        """
        self.opponent = opponent


    def get_legal_moves(self, board):
        """Enumerates all possible moves for player and returns
        them as a list of move objects.
        :param Board board: the board object currently used
        :return: list of legal move objects
        """
        legal_moves = []
        
        for row in range(board.size):
            for col in range(board.size):
                neighbors = []
                # list of 3-tuples: (from_coords, dir, neigh_coords)
                if board.matrix[row][col] == self.piece_type:
                    if col - 1 >= 0 and \
                       board.get_space((row, col-1)) == self.opponent_type:
                            neighbors += [((row, col), "W", (row, col-1))]
                    if col + 1 < board.size and \
                       board.matrix[row][col+1] == self.opponent_type:
                            neighbors += [((row, col), "E", (row, col+1))]
                    if row - 1 >= 0 and \
                       board.matrix[row-1][col] == self.opponent_type:
                            neighbors += [((row, col), "N", (row-1, col))]
                    if row + 1 < board.size and \
                       board.matrix[row+1][col] == self.opponent_type:
                            neighbors += [((row, col), "S", (row+1, col))]
                # neighbors is a list of neighboring coordinates
                    # that have enemy pieces

                # check if we can jump over neighbors
                i = 0
                while i < len(neighbors):
                    n = neighbors[i]
                    from_coords = n[0]
                    direc = n[1]
                    opp_coords = n[2]
                    new_coords = (opp_coords[0] + MOVE_DICT[direc][0], opp_coords[1] + MOVE_DICT[direc][1])
                    if board.on_board(new_coords) and board.get_space(new_coords) == BLANK_SPACE:
                        nmove = Move(from_coords, new_coords, direc)
                        legal_moves.append(nmove)
                        # see if we need to consider hopping
                        next_neigh = (new_coords[0] + MOVE_DICT[direc][0], new_coords[1] + MOVE_DICT[direc][1])
                        if board.on_board(next_neigh) and board.get_space(next_neigh) == self.opponent_type:
                            neighbors.append((from_coords, direc, next_neigh))
                    i += 1
        return legal_moves

    def eval_board(self, board):
        """Returns score of player's current standing in game as a float.
        :param Board board: board object to be evaluated
        """
        move_metric = 4
        self_num_moves = len(self.get_legal_moves(board))
        if self_num_moves == 0:
            return NEG_INF
        
        self_pieces = board.get_num_pieces(self.piece_type)
        self_score = self_num_moves*move_metric + self_pieces

        opp_num_moves = len(self.opponent.get_legal_moves(board))
        if opp_num_moves == 0:
            return INFINITY
        
        opp_pieces = board.get_num_pieces(self.opponent.piece_type)
        opp_score = opp_num_moves*move_metric + opp_pieces

        score = self_score - opp_score
        return score

    def minimax_std(self, board, move, depth, evals, num_branches,
                    depth_bound):
        """Searches for best move for player by evaluating possible
        courses of action using a modified minimax algorithm and returns it.
        :param Board board: board object to be evaluated
        :param Move move: move object executed to arrive at input board
        :param int depth: current depth of alph-bet minimax algorithm
        :param int evals: number of evaluations made so far
        :param int num_branches: number of branches created so far
        :param int depth_bound: depth bound of minimax algorithm
        :return: tuple of best move's score, the move object,
                number of evals, and number of branches
        """
        if depth >= depth_bound:
            return self.eval_board(board), move, evals+1, num_branches

        if depth % 2 == 0:  # max node
            cbv = NEG_INF
            best_move = None
            legal_moves = self.get_legal_moves(board)
            branching = len(legal_moves)
            num_branches.append(branching)
            for legal_move in legal_moves:
                new_board = deepcopy(board)
                new_board.make_move(legal_move)
                bv, new_move, evals, num_branches = self.minimax_std(new_board,
                        legal_move, depth+1, evals, num_branches, depth_bound)
                if bv > cbv:
                    cbv = bv
                    best_move = new_move
            if move:
                return cbv, move, evals, num_branches
            elif best_move:
                return cbv, best_move, evals, num_branches
            else:  # going to lose...
                return cbv, legal_moves[0], evals, num_branches
        else:
            cbv = INFINITY
            best_move = None
            legal_moves = self.get_legal_moves(board)
            branching = len(legal_moves)
            num_branches.append(branching)
            for legal_move in legal_moves:
                new_board = deepcopy(board)
                new_board.make_move(legal_move)
                bv, new_move, evals, num_branches = self.minimax_std(new_board, 
                        legal_move, depth+1, evals, num_branches, depth_bound)
                if bv < cbv:
                    cbv = bv
                    best_move = new_move
            if move:
                return cbv, move, evals, num_branches
            else:
                return cbv, best_move, evals, num_branches

    def minimax_alp_bet(self, board, move, alpha, beta, depth, evals, 
			num_branches, cutoffs, depth_bound):
        """Searches for best move for player by evaluating possible
        courses of action using a modified alpha beta pruning minimax
        algorithm and returns it.
        :param Board board: board object to be evaluated
        :param Move move: move object executed to arrive at input board
        :param int alpha: alpha value for alph-bet minimax algorithm
        :param int beta: beta value for alph-bet minimax algorithm
        :param int depth: current depth of alph-bet minimax algorithm
        :return: tuple of best move's score, best move object, and # of evals
        """
        #returns (pbv, move)
        # even depth -> max, odd depth -> min
        # move is the move that was executed to get this board
        if depth >= depth_bound:
            return self.eval_board(board), move, evals+1, num_branches, cutoffs
        
        if depth % 2 == 0:  # max node/self's turn
            best_move = None
            legal_moves = self.get_legal_moves(board)
            branching = len(legal_moves)
            num_branches.append(branching)
            for legal_move in legal_moves:
                new_board = deepcopy(board)
                new_board.make_move(legal_move)
                bv, new_move, evals, num_branches, cutoffs =\
                 self.minimax_alp_bet(new_board, legal_move, alpha,
                    beta, depth+1, evals, num_branches, cutoffs, depth_bound)
                if bv > alpha:
                    alpha = bv
                    best_move = new_move
                if alpha >= beta:
                    cutoffs += 1
                    if move:
                        return beta, move, evals, num_branches, cutoffs
                    else:
                        return beta, best_move, evals, num_branches, cutoffs
            if move:
                return alpha, move, evals, num_branches, cutoffs
            elif best_move:
                return alpha, best_move, evals, num_branches, cutoffs
            else:
                return alpha, legal_moves[0], evals, num_branches, cutoffs

        else:  # min node/opponent's turn
            best_move = None
            legal_moves = self.opponent.get_legal_moves(board)
            branching = len(legal_moves)
            num_branches.append(branching)
            for legal_move in legal_moves:
                new_board = deepcopy(board)
                new_board.make_move(legal_move)
                bv, new_move, evals, num_branches, cutoffs =\
                 self.minimax_alp_bet(new_board, legal_move, alpha,
                    beta, depth+1, evals, num_branches, cutoffs, depth_bound)
                if bv < beta:
                    beta = bv
                    best_move = new_move
                if beta <= alpha:
                    cutoffs += 1
                    if move:
                        return alpha, move, evals, num_branches, cutoffs
                    else:
                        return alpha, best_move, evals, num_branches, cutoffs
            if move:
                return beta, move, evals, num_branches, cutoffs
            else:
                return beta, best_move, evals, num_branches, cutoffs

    def minimax(self, board, depth_bound, with_pruning):
            """Function handler for both minimax algorithms.
            :param Board board: board object to be evaluated
            :param int depth_bound: depth bound for minimax algorithms
            :param bool with_pruning: use alpha beta pruning version or not
            :return: score as float, move object, # of evals, and # of cutoffs
            """
            if with_pruning:
                return self.minimax_alp_bet(board, None, NEG_INF, INFINITY,
                 0, 0, [], 0, depth_bound)
            else:
                score, move, evals, num_branches =\
                 self.minimax_std(board, None, 0, 0, [], depth_bound)
                return score, move, evals, num_branches, 0  # 0 cutoffs
