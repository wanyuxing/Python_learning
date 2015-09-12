"""
Monte Carlo Tic-Tac-Toe Player - Henry Wan. This program can only
run on http://www.codeskulptor.org
"""

import random
import poc_ttt_gui
import poc_ttt_provided as provided

# Constants for Monte Carlo simulator
NTRIALS = 100        # Number of trials to run
SCORE_CURRENT = 1.0 # Score for squares played by the current player
SCORE_OTHER = 1.0   # Score for squares played by the other player

def mc_trial(board, player):
    """
    This function takes a current board and the next player to move. 
    The function should play a game starting with the given player 
    by making random moves, alternating between players. 
    The function should return nothing when the game is over.
    """
    winner = None
    
    while winner == None:
        # Move
        empt = board.get_empty_squares()
        random_num = random.randrange(len(empt))
        row, col = empt[random_num]
        board.move(row, col, player)

        # Update state
        winner = board.check_win()
        player = provided.switch_player(player)
        
    return

def mc_update_scores(scores, board, player):
    """
    This function takes a grid of scores (a list of lists) with the same dimensions 
    as the Tic-Tac-Toe board, a board from a completed game, and which player 
    the machine player is. The function should score the completed board and update 
    the scores grid. As the function updates the scores grid directly, it does not 
    return anything.
    """            
    if (board.check_win() == player):
        for row in range(board.get_dim()):
            for col in range(board.get_dim()):
                if (board.square(row, col) == player):
                    scores[row][col] += SCORE_CURRENT
                elif (board.square(row, col) == provided.switch_player(player)):
                    scores[row][col] -= SCORE_OTHER                 
    elif (board.check_win() == provided.switch_player(player)):
        for row in range(board.get_dim()):
            for col in range(board.get_dim()):
                if (board.square(row, col) == player):
                    scores[row][col] -= SCORE_CURRENT
                elif (board.square(row, col) == provided.switch_player(player)):
                    scores[row][col] += SCORE_OTHER                    
    return

def get_best_move(board, scores):
    """
    This function takes a current board and a grid of scores. The function should 
    find all of the empty squares with the maximum score and randomly return one 
    of them as a (row, column) tuple.
    """
    max_num = 0
    maxlist = []
    empt = board.get_empty_squares()
    
    if (len(empt) == 0):
        return
    else:
        for pos in empt:
            if (scores[pos[0]][pos[1]] > max_num):
                max_num = scores[pos[0]][pos[1]]
        for pos in empt:
            if (scores[pos[0]][pos[1]] == max_num):
                maxlist.append(pos)
        return maxlist[random.randrange(len(maxlist))]

def mc_move(board, player, trials):
    """
    This function takes a current board, which player the machine player is, and 
    the number of trials to run. The function should use the Monte Carlo simulation 
    to return a move for the machine player in the form of a (row, column) tuple.
    """
    scores = [[0 for dummycol in range(board.get_dim())] 
                           for dummyrow in range(board.get_dim())]
    count = 0
    while (count < trials):
        boardclone = board.clone()
        mc_trial(boardclone, player)
        mc_update_scores(scores, boardclone, player)
        count += 1
    pos = get_best_move(board, scores)
    return pos[0], pos[1]
    
# Test game with the console or the GUI.  Uncomment whichever 
# you prefer.  Both should be commented out when you submit 
# for testing to save time.

#provided.play_game(mc_move, NTRIALS, False)        
poc_ttt_gui.run_gui(3, provided.PLAYERX, mc_move, NTRIALS, False)