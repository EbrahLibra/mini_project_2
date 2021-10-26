import time
from search_algorithm import SearchAlgorithm
from simple_heuristic import SimpleHeuristic
from complex_heuristic import ComplexHeuristic
from base_heuristic import BaseHeuristic


class Game:
    HUMAN = 0
    AI = 1

    # TODO: Add following parameters:
    # - the maximum depth of the adversarial search for player 1 and for player 2 (d1, d2)
    # - the maximum allowed time (in seconds) for your program to return a move (t)
    # - a Boolean to force the use of either minimax (FALSE) or alphabeta (TRUE) (a)
    # - the play modes - H-H, H-AI, AI-H and AI-AI (pm)
    def __init__(self,
                 board_dimension=3,
                 block_number: int = 0,
                 block_positions: list = None,
                 winning_line_size=3,
                 recommend=True):
        self._board_dimension = board_dimension
        self._block_number = block_number
        self._block_positions = block_positions
        self._winning_line_size = winning_line_size
        self.recommend = recommend
        self.player_turn = None
        self.current_state = []
        self.initialize_game()

    def initialize_game(self):
        for i in range(self._board_dimension):
            self.current_state.append(['.'] * self._board_dimension)

        # X always starts
        self.player_turn = 'X'

    def add_blocks(self):
        for coordinates in self._block_positions:
            self.current_state[coordinates[0]][coordinates[1]] = 'B'

    def draw_board(self):
        print()
        self.add_blocks()
        print("Current board state:")
        for y in range(self._board_dimension):
            for x in range(self._board_dimension):
                print(F'{self.current_state[x][y]}', end="")
            print()
        print()

    # 'B' is for a block at that position
    def is_valid(self, px, py):
        if px < 0 or px >= self._board_dimension or py < 0 or py >= self._board_dimension:
            return False
        elif self.current_state[px][py] != '.':
            return False
        elif self.current_state[px][py] == 'B':
            return False
        else:
            return True

    # Returns . if tie, X if X wins, 0 if 0 wins
    def is_end(self) -> str:
        winner = self.check_diagonal_board_win(self.current_state, self._winning_line_size)
        winner = self.check_horizontal_win(self.current_state, self._winning_line_size) if winner == None else winner
        winner = self.check_vertical_board_win(self.current_state, self._winning_line_size) if winner == None else winner
        return winner

    def check_end(self):
        self.result = self.is_end()
        # Printing the appropriate message if the game has ended
        if self.result != None:
            if self.result == 'X':
                print('The winner is X!')
            elif self.result == 'O':
                print('The winner is O!')
            elif self.result == '.':
                print("It's a tie!")
            self.initialize_game()
        return self.result

    def input_move(self):
        while True:
            print(F'Player {self.player_turn}, enter your move:')
            entry = input('enter the x coordinate: ')
            while not self.is_integer(entry):
                entry = input('Please, enter an integer value! waiting:')
            else:
                px = int(entry)
            entry = input('enter the y coordinate:')
            while not self.is_integer(entry):
                entry = input('Please, enter an integer value! waiting:')
            else:
                py = int(entry)
            if self.is_valid(px, py):
                return (px, py)
            else:
                print('The move is not valid! Try again.')

    def is_integer(self, value):
        isInteger = False
        try:
            value = int(value)
            isInteger = True
        except ValueError:
            pass
        return isInteger

    def switch_player(self):
        if self.player_turn == 'X':
            self.player_turn = 'O'
        elif self.player_turn == 'O':
            self.player_turn = 'X'
        return self.player_turn

    # XXX: Uncomment when AI added components
    def play(self,
             # algo: SearchAlgorithm = 1,
             player_x=None,
             player_o=None):

        if player_x == None:
            player_x = self.HUMAN

        if player_o == None:
            player_o = self.HUMAN

        while True:
            self.draw_board()

            if self.check_end():
                return

            # start = time.time()
            #
            # if self.player_turn == 'X':
            #     (m, x, y) = algo.evaluate(max=True)
            # else:
            #     (m, x, y) = algo.evaluate(max=False)
            #
            # end = time.time()
            (x, y) = (0, 0)
            if (self.player_turn == 'X' and player_x == self.HUMAN) or (
                    self.player_turn == 'O' and player_o == self.HUMAN):
                # if self.recommend:
                #     print(F'Evaluation time: {round(end - start, 7)}s')
                #     print(F'Recommended move: x = {x}, y = {y}')
                (x, y) = self.input_move()
            # if (self.player_turn == 'X' and player_x == self.AI) or (self.player_turn == 'O' and player_o == self.AI):
            #     print(F'Evaluation time: {round(end - start, 7)}s')
            #     print(F'Player {self.player_turn} under AI control plays: x = {x}, y = {y}')
            self.current_state[x][y] = self.player_turn
            self.switch_player()

    def _win_in_vertical_board_segment(self, x) -> str:
        for i in range(self._board_dimension - self._winning_line_size):
            end_segment = i + self._winning_line_size
            # Segment contains only
            if all(element == self.current_state[x][i] for element in self.current_state[x][i:end_segment]):
                return self.current_state[x][i]
        return ''

    def check_diagonal_board_win(self, board, success_factor):
        length = len(board)
        x_expected_winning_criteria = 'X' * success_factor
        o_expected_winning_criteria = 'O' * success_factor
        for column in range(length):
            target_diagonal = ''
            for row, row_list in enumerate(board):
                if 0 <= column + row < length:
                    target_diagonal += row_list[column + row]
            if x_expected_winning_criteria in target_diagonal:
                return 'X'
            elif o_expected_winning_criteria in target_diagonal:
                return 'O'
        for column in reversed(range(-(length - 1), 1)):
            target_diagonal = ''
            for row, row_list in enumerate(board):
                if 0 <= column + row < length:
                    target_diagonal += row_list[column + row]
            if x_expected_winning_criteria in target_diagonal:
                return 'X'
            elif o_expected_winning_criteria in target_diagonal:
                return 'O'
        for column in reversed(range(length)):
            target_diagonal = ''
            for row, row_list in enumerate(board):
                if 0 <= column - row < length:
                    target_diagonal += row_list[column - row]
            if x_expected_winning_criteria in target_diagonal:
                return 'X'
            elif o_expected_winning_criteria in target_diagonal:
                return 'O'
        for column in range(length):
            target_diagonal = ''
            for row, row_list in enumerate(reversed(board)):
                if 0 <= column + row < length:
                    target_diagonal += row_list[column + row]
            if x_expected_winning_criteria in target_diagonal:
                return 'X'
            elif o_expected_winning_criteria in target_diagonal:
                return 'O'

    def check_vertical_board_win(self, board, success_factor) -> str:
        x_expected_winning_criteria = 'X' * success_factor
        o_expected_winning_criteria = 'O' * success_factor
        target_column = ''
        for column in range(len(board) - 1):
            for row_list in board:
                target_column += row_list[column]
            if x_expected_winning_criteria in target_column:
                return 'X'
            elif o_expected_winning_criteria in target_column:
                return 'O'
            target_column = ''

    def check_horizontal_win(self, board, success_factor) -> str:
        x_expected_winning_criteria = 'X' * success_factor
        o_expected_winning_criteria = 'O' * success_factor
        for row in range(len(board) - 1):
            target_row = ''.join(board[row])
            if x_expected_winning_criteria in target_row:
                return 'X'
            elif o_expected_winning_criteria in target_row:
                return 'O'


def main():
    g = Game(board_dimension=5, block_positions=[(0, 1), (0, 2)])
    g.play()


if __name__ == "__main__":
    main()
