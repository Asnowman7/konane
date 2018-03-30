'''
konane main file
Austin Wan & Alex Snow
'''

import game_analysis as game
import random
import pdb
import csv
import timeit

ANALYSIS_MODE = False
# if ANALYSIS_MODE:
#         import matplotlib.pyplot as plt
        
O_PIECE = "O"
X_PIECE = "X"
BLANK_SPACE = "."
INFINITY = float("inf")
NEG_INF = float("-inf")
CPU_EVALS = []
CPU_CUTOFFS = []
HUM_EVALS = []
CPU_BRANCHING = []
HUM_BRANCHING = []
CPU_AVG_TIMES = []
HUM_AVG_TIMES = []


def start_board(board, size, cpu_first):
    """Prepares input board object to start game.
    :param Board board: board object to be prepared.
    :param int size: length of both dimensions of board
    :param bool cpu_first: whether its the cpu's turn first or not
    """
    first_moves = [(0,0), (size//2-1, size//2-1),
                   (size//2, size//2), (size-1, size-1)]
    if cpu_first:
        i = random.randint(0, 3)
        first_remove = first_moves[i]
        board.change_space(first_remove, game.BLANK_SPACE)
        print(board)
        wait_for_response = True
        while wait_for_response:
            print("Which O piece do you want to remove?")
            options = ["1) E neighbor\n2) S neighbor",
                "1) N neighbor\n2) S neighbor\n3) E neighbor\n4) W neighbor",
                "1) N neighbor\n2) S neighbor\n3) E neighbor\n4) W neighbor",
                "1) N neighbor\n2) W neighbor",]
            move_opt = [[(0,1), (1, 0)], [(size//2-2, size//2-1),
                        (size//2, size//2-1), (size//2-1, size//2),
                        (size//2-1, size//2-2)], [(size//2-1, size//2),
                        (size//2+1, size//2), (size//2, size//2+1),
                        (size//2, size//2-1)], [(size-2, size-1),
                        (size-1, size-2)]]
            print(options[i])
            prompt_2 = int(input(">> "))
            # prompt_2 = random.randint(0, 3)
            if (prompt_2 in [1, 2]) or (i in [1, 2] and prompt_2 in [3, 4]):
                board.change_space(move_opt[i][prompt_2-1], game.BLANK_SPACE)
                wait_for_response = False
            else:
                print("Please pick a number")
    else:
        print(board)
        wait_for_response = True
        while wait_for_response:
                
            print("""Which piece do you want to remove first?
                    1) NW corner 
                    2) NW center
                    3) SE center
                    4) SE corner""")
            prompt_2 = int(input(">> "))
            # prompt_2 = random.randint(0, 3)
            if prompt_2 in [1, 2, 3, 4]:
                    board.change_space(
                        first_moves[prompt_2-1], game.BLANK_SPACE)
                    move_opt = [[(0,1), (1, 0)], [(size//2-2, size//2-1),
                                (size//2, size//2-1), (size//2-1, size//2),
                                (size//2-1, size//2-2)], [(size//2-1, size//2),
                                (size//2+1, size//2), (size//2, size//2+1),
                                (size//2, size//2-1)], [(size-2, size-1),
                                (size-1, size-2)]]
                    board.change_space(random.choice(
                        move_opt[prompt_2-1]), game.BLANK_SPACE)
                    wait_for_response = False
            else:
                    print("Please input 1, 2, 3 or 4")

def get_player_move(board, size, player):
    """Prompts human player to input move, verifies it, then returns it.
    :param Board board: board object used to play game
    :param int size: size of both dimensions of board
    :param Player player: player object of human player
    """
    legal_options = range(1, size+1)
    while True:  # breaks when there is a legal move to return
            row_from = int(input(
                "Pick row of piece you'd like to move (-1 to undo move) >> "))
            if row_from == -1:
                    print("Undoing last round of moves.")
                    board.undo_move()
                    print(board)
                    continue
            if row_from not in legal_options:
                    print("Sorry, that's not a legal row.")
                    continue
            col_from = int(input(
                "Pick column of piece you'd like to move >> "))
            if col_from not in legal_options:
                    print("Sorry, that's not a legal column.")
                    continue
            row_from -= 1  # since indexing starts at 0, not 1
            col_from -= 1
            if board.get_space((row_from, col_from)) != player.piece_type:
                    print("Sorry, you don't have a piece there.")
                    continue

            row_to = int(input(
                "Pick row of the space you'd like to move to >> "))
            if row_to not in legal_options:
                    print("Sorry, that's not a legal row.")
                    continue
            col_to = int(input(
                "Pick column of the space you'd like to move to >> "))
            if col_to not in legal_options:
                    print("Sorry, that's not a legal column.")
                    continue
            row_to -= 1  # since indexing starts at 0, not 1
            col_to -= 1

            input_direc = ""
            delta_row = row_to - row_from
            delta_col = col_to - col_from

            if delta_row != 0:
                    if delta_row > 0:
                            input_direc = "S"
                    else:
                            input_direc = "N"
            else:
                    if delta_col > 0:
                            input_direc = "E"
                    else:
                            input_direc = "W"

            input_move = game.Move((row_from, col_from),
                (row_to, col_to), input_direc)
            legal_moves = player.get_legal_moves(board)

            move_is_legal = False
            for move in legal_moves:
                    if input_move.compare_move(move):
                            move_is_legal = True
                            break

            if not move_is_legal:
                    print("Sorry, that's not a legal move.")
                    continue

            return input_move

def post_game_eval(cpu_total_evals, cpu_list_avg_branch, cpu_total_cutoffs,
 cpu_avg_time, hum_total_evals, hum_list_avg_branch, hum_avg_time):
    """Compiles data from previous game to global data lists."""
    hum_total_avg_branch = \
        sum(hum_list_avg_branch) / float(len(hum_list_avg_branch))
    cpu_total_avg_branch = \
        sum(cpu_list_avg_branch) / float(len(cpu_list_avg_branch))
    print("Stats for minimax with alpha beta pruning:")
    print("Number of static evaluations: ", cpu_total_evals)
    print("Average branching factor: ", cpu_total_avg_branch)
    print("Number of cutoffs: ", cpu_total_cutoffs)
    print("\n")
    print("Stats for standard minimax:")
    print("Number of static evaluations: ", hum_total_evals)
    print("Average branching factor: ", hum_total_avg_branch)
    print("\n")
    CPU_BRANCHING.append(cpu_total_avg_branch)
    HUM_BRANCHING.append(hum_total_avg_branch)
    CPU_EVALS.append(cpu_total_evals)
    CPU_CUTOFFS.append(cpu_total_cutoffs)
    HUM_EVALS.append(hum_total_evals)
    CPU_AVG_TIMES.append(cpu_avg_time)
    HUM_AVG_TIMES.append(hum_avg_time)

def main():
    """Starts game of Konane."""
    size = 8
    board = game.Board(size)
    options = ["y", "n"]
    depth_bound_prompt = \
        input("Input the depth bound of minimax algorithm (4 recommended) >> ")
    game.DEPTH_BOUND = int(depth_bound_prompt)
    first_move_prompt = input("Is the CPU going first? (y/n) >> ").lower()
    cpu_first = False
    cpu_piece = O_PIECE
    player_piece = X_PIECE
    if "y" in first_move_prompt:
        cpu_first = True
        cpu_piece = X_PIECE
        player_piece = O_PIECE

    # initialize player objects
    human_player = game.Player(True, player_piece)
    cpu_player = game.Player(False, cpu_piece)
    human_player.assign_opponent(cpu_player)
    cpu_player.assign_opponent(human_player)

    start_board(board, size, cpu_first)  # mutates board
    print(board)
    cpu_turn = cpu_first

    if ANALYSIS_MODE:
        # cpu uses minimax_alp_beta
        cpu_total_evals = 0
        cpu_list_avg_branch = []
        cpu_total_cutoffs = 0
        cpu_total_time = 0
        cpu_moves_made = 0
        # hum uses minimax_std without alp_beta_pruning
        hum_total_evals = 0
        hum_list_avg_branch = []
        hum_total_time = 0
        hum_moves_made = 0

    while True:
        print(board)
        if cpu_turn:
            # call minimax and make a move
            with_pruning = True
            depth = game.DEPTH_BOUND
            ts = timeit.default_timer()  # start timer
            score, cpu_move, evals, num_branches, cut_offs =\
             cpu_player.minimax(board, depth, with_pruning)
            te = timeit.default_timer()  # end timer

            if ANALYSIS_MODE:
                cpu_total_time += te - ts
                cpu_moves_made += 1
                print("depth is ", depth)
                print("debug - cpu's score is ", score)
                print("debug - cpu's move is ", cpu_move)
                print("debug - cpu made %d static evaluations." %evals)
                if (score != INFINITY) and (score != NEG_INF):
                    avg_branch_factor = \
                        sum(num_branches) / float(len(num_branches))
                    print("debug - cpu's avg branching factor is %f."
                          %avg_branch_factor)
                    print("debug - cpu made %d cutoffs." %cut_offs)
                    cpu_list_avg_branch += [avg_branch_factor]
                cpu_total_evals += evals
                cpu_total_cutoffs += cut_offs
                    
            board.make_move(cpu_move)
            cpu_turn = False
            
        else:
            if ANALYSIS_MODE:
                # CPU using minimax_std
                with_pruning = False
                depth = game.DEPTH_BOUND
                ts = timeit.default_timer()  # start timer
                score, player_move, evals, num_branches, cut_offs =\
                 human_player.minimax(board, depth, with_pruning)
                te = timeit.default_timer()  # end timer
                hum_total_time += te - ts
                hum_moves_made += 1
                print("depth is ", depth)
                print("debug - player's score is ", score)
                print("debug - player's move is ", player_move)
                print("debug - player made %d static evaluations." %evals)
                if (score != INFINITY) and (score != NEG_INF):
                    avg_branch_factor = \
                        sum(num_branches) / float(len(num_branches))
                    print("debug - player's avg branching factor is %f."
                          %avg_branch_factor)
                    print("debug - player made %d cutoffs." %cut_offs)
                    hum_list_avg_branch += [avg_branch_factor]
                hum_total_evals += evals
                board.make_move(player_move)
                cpu_turn = True
            else:
                # human player giving move
                player_move = get_player_move(board, size, human_player)
                board.make_move(player_move)  # mutates board
                cpu_turn = True  

        # check status of game
        if ANALYSIS_MODE:
            if not cpu_turn and len(human_player.get_legal_moves(board)) == 0:
                print(board)
                print("Computer wins")
                cpu_avg_time = cpu_total_time/float(cpu_moves_made)
                hum_avg_time = hum_total_time/float(hum_moves_made)
                post_game_eval(cpu_total_evals, cpu_list_avg_branch,
                    cpu_total_cutoffs, cpu_avg_time, hum_total_evals,
                               hum_list_avg_branch, hum_avg_time)
                return True
            if cpu_turn and len(cpu_player.get_legal_moves(board)) == 0:
                print(board)
                print("You win!")
                cpu_avg_time = cpu_total_time/float(cpu_moves_made)
                hum_avg_time = hum_total_time/float(hum_moves_made)
                post_game_eval(cpu_total_evals, cpu_list_avg_branch,
                    cpu_total_cutoffs, cpu_avg_time, hum_total_evals,
                               hum_list_avg_branch, hum_avg_time)
                return False
        else:
            if not cpu_turn and len(human_player.get_legal_moves(board)) == 0:
                print(board)
                print("Computer wins")
                return True
            if cpu_turn and len(cpu_player.get_legal_moves(board)) == 0:
                print(board)
                print("You win!")
                return False

def exp_data_generator():
    """Simulates multiple games cpu vs. cpu, collects data, plots it,
    and writes it to a csv.
    """
    cpu_wins = 0
    player_wins = 0
    test_depths = 6  # test up to this depth
    num_tests = 10
    results = "CPU Starts:\n"
    for i in range(test_depths):
        for j in range(num_tests):
            if main(i+1):
                cpu_wins += 1
            else:
                player_wins += 1

    results += \
        "CPU won %d times.\nPlayer won %d times.\n" %(cpu_wins, player_wins)
    print(results)

    # analysis
    # plt.figure(1)
    # plt.xlabel('Depth', fontsize=14, color='red')
    # plt.ylabel('Number of Static Evaluations', fontsize=14, color='blue')
    # plt.title('Static Evaluations in minimax_std and minimax_alp_bet')
    # plt.plot(range(1, num_tests+1), HUM_EVALS)
    # plt.plot(range(1, num_tests+1), CPU_EVALS)

    # plt.figure(2)
    # plt.xlabel('Depth', fontsize=14, color='red')
    # plt.ylabel('Number of Static Evaluations', fontsize=14, color='blue')
    # plt.title('Evaluations and Cutoffs in minimax_alp_bet')
    # plt.plot(range(1, num_tests+1), CPU_EVALS)
    # plt.plot(range(1, num_tests+1), CPU_CUTOFFS)

    # plt.figure(3)
    # plt.xlabel('Depth', fontsize=14, color='red')
    # plt.ylabel('Average Branchign Factor', fontsize=14, color='blue')
    # plt.title('Average Branching Factor in minimax_std and minimax_alp_bet')
    # plt.plot(range(1, num_tests+1), CPU_BRANCHING)
    # plt.plot(range(1, num_tests+1), HUM_BRANCHING)
    # plt.show()


    with open('konane_analysis.csv', 'ab') as csvfile:
        datawriter = csv.writer(csvfile, delimiter=',')
        # HUM_EVALS, HUM_BRANCHING, CPU_EVALS, CPU_CUTOFFS, CPU_BRANCHING
        length = len(HUM_EVALS)
        datawriter.writerow(["Depth", "# of minimax_std evals",
            "Avg branching factor of minimax_std",
            "Avg exec time of minimax_std", "# of minimax_alph_bet evals", 
            "# of minimax_alph_bet cutoffs",
            "Avg branching factor of minimax_alph_bet", 
            "Avg exec time of minimax_alph_bet"])
        for i in range(length):
            datawriter.writerow([1+i//num_tests, HUM_EVALS[i],
                HUM_BRANCHING[i], HUM_AVG_TIMES[i], CPU_EVALS[i],
                CPU_CUTOFFS[i], CPU_BRANCHING[i], CPU_AVG_TIMES[i]])

main()
