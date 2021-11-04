from base_heuristic import BaseHeuristic


class ComplexHeuristic(BaseHeuristic):
    """
    Complex function
    :param board: Testing board
    :param success_factor: the number of peaces to win
    """
    def __init__(self, success_factor):
        self._success_factor = success_factor

    """
    :return: difference number of options for both players
    """
    def calculate_value(self, board) -> int:
        # diagonal analysis
        length = len(board)
        x_expected_winning_criteria = 'X' * self._success_factor
        o_expected_winning_criteria = 'O' * self._success_factor

        x_diagonal_chances = 0
        o_diagonal_chances = 0
        for column in range(1, length):
            target_diagonal = ''
            for row, row_list in enumerate(board):
                if 0 <= column + row < length:
                    target_diagonal += row_list[column + row]
            if len(target_diagonal) >= self._success_factor:
                if x_expected_winning_criteria in target_diagonal.replace('.', 'X'):
                    x_diagonal_chances += 1
                if o_expected_winning_criteria in target_diagonal.replace('.', 'O'):
                    o_diagonal_chances += 1
        for column in reversed(range(-(length - 1), 1)):
            target_diagonal = ''
            for row, row_list in enumerate(board):
                if 0 <= column + row < length:
                    target_diagonal += row_list[column + row]
            if len(target_diagonal) >= self._success_factor:
                if x_expected_winning_criteria in target_diagonal.replace('.', 'X'):
                    x_diagonal_chances += 1
                if o_expected_winning_criteria in target_diagonal.replace('.', 'O'):
                    o_diagonal_chances += 1
        for column in reversed(range(length)):
            target_diagonal = ''
            for row, row_list in enumerate(board):
                if 0 <= column - row < length:
                    target_diagonal += row_list[column - row]
            if len(target_diagonal) >= self._success_factor:
                if x_expected_winning_criteria in target_diagonal.replace('.', 'X'):
                    x_diagonal_chances += 1
                if o_expected_winning_criteria in target_diagonal.replace('.', 'O'):
                    o_diagonal_chances += 1
        for column in range(1, length):
            target_diagonal = ''
            for row, row_list in enumerate(reversed(board)):
                if 0 <= column + row < length:
                    target_diagonal += row_list[column + row]
            if len(target_diagonal) >= self._success_factor:
                if x_expected_winning_criteria in target_diagonal.replace('.', 'X'):
                    x_diagonal_chances += 1
                if o_expected_winning_criteria in target_diagonal.replace('.', 'O'):
                    o_diagonal_chances += 1

        x_vertical_chances = 0
        o_vertical_chances = 0
        for column in range(length):
            target_column = ''
            for row_list in board:
                target_column += row_list[column]
            if x_expected_winning_criteria in target_column.replace('.', 'X'):
                x_vertical_chances += 1
            if o_expected_winning_criteria in target_column.replace('.', 'O'):
                o_vertical_chances += 1

        x_horizontal_chances = 0
        o_horizontal_chances = 0
        for row in range(length - 1):
            target_row = ''.join(board[row])
            if x_expected_winning_criteria in target_row.replace('.', 'X'):
                x_horizontal_chances += 1
            if o_expected_winning_criteria in target_row.replace('.', 'O'):
                o_horizontal_chances += 1

        total_x_n_options = x_diagonal_chances + x_vertical_chances + x_horizontal_chances
        total_o_n_options = o_diagonal_chances + o_vertical_chances + o_horizontal_chances

        return total_x_n_options - total_o_n_options
