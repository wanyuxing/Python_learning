"""
Project 4 - Dynamic Programming
@Author: Henry Wan
"""

def build_scoring_matrix(alphabet, diag_score, off_diag_score, dash_score):
    """
    The function returns a dictionary of dictionaries whose entries are 
    indexed by pairs of characters in alphabet plus '-'
    """
    alphabet_new = alphabet.copy()
    alphabet_new.add('-')
    matrix = dict()
    for i_idx in alphabet_new:
        new = dict()
        for j_idx in alphabet_new:
            if (i_idx == '-' or j_idx == '-'):
                new[j_idx] = dash_score
            elif (i_idx == j_idx):
                new[j_idx] = diag_score
            else:
                new[j_idx] = off_diag_score
        matrix[i_idx] = new
    return matrix

def compute_alignment_matrix(seq_x, seq_y, scoring_matrix, global_flag):
    """
    The function computes and returns the alignment matrix for seq_x and seq_y
    """
    length_m = len(seq_x)
    length_n = len(seq_y)
    matrix = [[0 for _ in range(length_n + 1)] for dummy in range(length_m + 1)]
    for i_idx in range(1, length_m + 1):
        matrix[i_idx][0] = matrix[i_idx - 1][0] + scoring_matrix[seq_x[i_idx - 1]]['-']
        if global_flag == False:
            matrix[i_idx][0] = max(0, matrix[i_idx][0])
    for j_idx in range(1, length_n + 1):
        matrix[0][j_idx] = matrix[0][j_idx - 1] + scoring_matrix['-'][seq_y[j_idx - 1]]
        if global_flag == False:
            matrix[0][j_idx] = max(0, matrix[0][j_idx]) 
    for i_idx in range(1, length_m + 1):
        for j_idx in range(1, length_n + 1):
            matrix[i_idx][j_idx] = max(matrix[i_idx - 1][j_idx - 1] + scoring_matrix[seq_x[i_idx - 1]][seq_y[j_idx - 1]],
                              matrix[i_idx - 1][j_idx] + scoring_matrix[seq_x[i_idx - 1]]['-'],
                              matrix[i_idx][j_idx - 1] + scoring_matrix['-'][seq_y[j_idx - 1]])
            if global_flag == False:
                matrix[i_idx][j_idx] = max(0, matrix[i_idx][j_idx])
    return matrix

def compute_global_alignment(seq_x, seq_y, scoring_matrix, alignment_matrix):
    """
    This function computes a global alignment of seq_x and seq_y using the 
    global alignment matrix alignment_matrix.
    """
    length_i = len(seq_x)
    length_j = len(seq_y)
    score = alignment_matrix[length_i][length_j]
    ans_x = ''
    ans_y = ''
    while (length_i != 0 and length_j != 0):
        if alignment_matrix[length_i][length_j] == alignment_matrix[length_i - 1][length_j - 1] + scoring_matrix[seq_x[length_i - 1]][seq_y[length_j - 1]]:
            ans_x = seq_x[length_i - 1] + ans_x
            ans_y = seq_y[length_j - 1] + ans_y
            length_i -= 1
            length_j -= 1
        else:
            if alignment_matrix[length_i][length_j] == alignment_matrix[length_i - 1][length_j] + scoring_matrix[seq_x[length_i - 1]]['-']:
                ans_x = seq_x[length_i - 1] + ans_x
                ans_y = '-' + ans_y
                length_i -= 1
            else:
                ans_x = '-' + ans_x
                ans_y = seq_y[length_j - 1] + ans_y
                length_j -= 1
    while length_i != 0:
        ans_x = seq_x[length_i - 1] + ans_x
        ans_y = '-' + ans_y
        length_i -= 1
    while length_j != 0:
        ans_x = '-' + ans_x
        ans_y = seq_y[length_j - 1] + ans_y
        length_j -= 1
    return (score, ans_x, ans_y)

def compute_local_alignment(seq_x, seq_y, scoring_matrix, alignment_matrix):
    """
    This function computes a local alignment of seq_x and seq_y using the local alignment matrix alignment_matrix
    """
    length_i = len(seq_x)
    length_j = len(seq_y)
    score = 0
    ans_x = ''
    ans_y = ''
    pos = [-1, -1]
    for i_idx in range(length_i + 1):
        for j_idx in range(length_j + 1):
            if alignment_matrix[i_idx][j_idx] > score:
                score = alignment_matrix[i_idx][j_idx]
                pos = [i_idx, j_idx]
    while alignment_matrix[pos[0]][pos[1]] != 0:
        if alignment_matrix[pos[0]][pos[1]] == alignment_matrix[pos[0] - 1][pos[1] - 1] + scoring_matrix[seq_x[pos[0] - 1]][seq_y[pos[1] - 1]]:
            ans_x = seq_x[pos[0] - 1] + ans_x
            ans_y = seq_y[pos[1] - 1] + ans_y
            pos[0] -= 1
            pos[1] -= 1
        else:
            if alignment_matrix[pos[0]][pos[1]] == alignment_matrix[pos[0] - 1][pos[1]] + scoring_matrix[seq_x[pos[0] - 1]]['-']:
                ans_x = seq_x[pos[0] - 1] + ans_x
                ans_y = '-' + ans_y
                pos[0] -= 1
            else:
                ans_x = '-' + ans_x
                ans_y = seq_y[pos[1] - 1] + ans_y
                pos[1] -= 1
    return (score, ans_x, ans_y)
    