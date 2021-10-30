import random

testBoard = [
    ['X', 'X', 'X'],
    ['X', '.', '.'],
    ['O', '.', '.'],
]


def e_1(board, success_factor):
    """
    Complex function
    :param board: Testing board
    :param success_factor: the number of peaces to win
    :return: difference number of options for both players
    """
    # diagonal analysis
    length = len(board)
    x_expected_winning_criteria = 'X' * success_factor
    y_expected_winning_criteria = 'O' * success_factor

    x_diagonal_chances = 0
    y_diagonal_chances = 0
    for column in range(1, length):
        target_diagonal = ''
        for row, row_list in enumerate(board):
            if 0 <= column + row < length:
                target_diagonal += row_list[column + row]
        if x_expected_winning_criteria in target_diagonal.replace('.', 'X'):
            x_diagonal_chances += 1
        if y_expected_winning_criteria in target_diagonal.replace('.', 'Y'):
            y_diagonal_chances += 1
    for column in reversed(range(-(length - 1), 1)):
        target_diagonal = ''
        for row, row_list in enumerate(board):
            if 0 <= column + row < length:
                target_diagonal += row_list[column + row]
        if x_expected_winning_criteria in target_diagonal.replace('.', 'X'):
            x_diagonal_chances += 1
        if y_expected_winning_criteria in target_diagonal.replace('.', 'Y'):
            y_diagonal_chances += 1
    for column in reversed(range(length)):
        target_diagonal = ''
        for row, row_list in enumerate(board):
            if 0 <= column - row < length:
                target_diagonal += row_list[column - row]
        if x_expected_winning_criteria in target_diagonal.replace('.', 'X'):
            x_diagonal_chances += 1
        if y_expected_winning_criteria in target_diagonal.replace('.', 'Y'):
            y_diagonal_chances += 1
    for column in range(1, length):
        target_diagonal = ''
        for row, row_list in enumerate(reversed(board)):
            if 0 <= column + row < length:
                target_diagonal += row_list[column + row]
        if x_expected_winning_criteria in target_diagonal.replace('.', 'X'):
            x_diagonal_chances += 1
        if y_expected_winning_criteria in target_diagonal.replace('.', 'Y'):
            y_diagonal_chances += 1
    print('X Diagonal chances ', x_diagonal_chances)
    print('Y Diagonal chances ', y_diagonal_chances)

    x_vertical_chances = 0
    y_vertical_chances = 0
    for column in range(len(board)):
        target_column = ''
        for row_list in board:
            target_column += row_list[column]
        if x_expected_winning_criteria in target_column.replace('.', 'X'):
            x_vertical_chances += 1
        if y_expected_winning_criteria in target_column.replace('.', 'Y'):
            y_vertical_chances += 1
    print('X Vertical chances ', x_vertical_chances)
    print('Y Vertical chances ', y_vertical_chances)

    x_horizontal_chances = 0
    y_horizontal_chances = 0
    for row in range(len(board) - 1):
        target_row = ''.join(board[row])
        if x_expected_winning_criteria in target_row:
            x_horizontal_chances += 1
        if y_expected_winning_criteria in target_row:
            y_horizontal_chances += 1

    print('X Horizontal chances ', x_horizontal_chances)
    print('Y Horizontal chances ', y_horizontal_chances)

    total_x_n_options = x_diagonal_chances + x_vertical_chances + x_horizontal_chances
    total_y_n_options = y_diagonal_chances + y_vertical_chances + y_horizontal_chances

    return total_x_n_options - total_y_n_options


def e_2(board_size, max=False):
    """
    Simple heuristic function
    :param board_size: the size of the board
    :param max: the player turn
    :return: the decisive value to make
    """
    if max:
        return -random.randint(0, board_size)
    else:
        return +random.randint(0, board_size)

