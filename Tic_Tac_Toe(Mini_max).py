"""
Mini-max Tic-Tac-Toe Player
@Author: Henry Wan
"""

import poc_ttt_gui
import poc_ttt_provided as provided

# Set timeout, as mini-max can take a long time
import codeskulptor
codeskulptor.set_timeout(60)

# SCORING VALUES - DO NOT MODIFY
SCORES = {provided.PLAYERX: 1,
          provided.DRAW: 0,
          provided.PLAYERO: -1}

def mm_move(board, player):
    """
    Make a move on the board.
    
    Returns a tuple with two elements.  The first element is the score
    of the given board and the second element is the desired move as a
    tuple, (row, col).
    """
    winner = board.check_win()
    if winner != None:
        return SCORES[winner], (-1, -1)

    ans_score = -2
    ans_pos = (-1, -1)
    for pos in board.get_empty_squares():
        board_new = board.clone()
        board_new.move(pos[0], pos[1], player)
        best_move_other = mm_move(board_new, provided.switch_player(player))
        score = best_move_other[0] * SCORES[player]
        if score == 1:
            return best_move_other[0], pos
        elif score == 0:
            ans_score = 0
            ans_pos = pos
        elif score > ans_score:
            ans_score = best_move_other[0]
            ans_pos = pos
    return ans_score, ans_pos

def move_wrapper(board, player, trials):
    """
    Wrapper to allow the use of the same infrastructure that was used
    for Monte Carlo Tic-Tac-Toe.
    """
    move = mm_move(board, player)
    assert move[1] != (-1, -1), "returned illegal move (-1, -1)"
    return move[1]

# Test game with the console or the GUI.
# Uncomment whichever you prefer.
# Both should be commented out when you submit for
# testing to save time.

#provided.play_game(move_wrapper, 1, False)        
poc_ttt_gui.run_gui(3, provided.PLAYERO, move_wrapper, 1, False)
