import time
from simple_heuristic import SimpleHeuristic
from complex_heuristic import ComplexHeuristic
from player import Player
# from search_algorithm import SearchAlgorithm
import random


class Game:
    MINIMAX = 0
    ALPHABETA = 1
    HUMAN = 2
    AI = 3

    # - param model_type: minimax (FALSE) or alphabeta (TRUE)
    # - param play_mode: H-H=0, H-AI=1, AI-H=2 and AI-AI=3 (pm)
    # - param p1_h_mode: if p1 is AI then simple heuristic (TRUE) or complex (FALSE)
    # - param p2_h_mode: if p2 is AI then simple heuristic (TRUE) or complex (FALSE)
    def __init__(self,
                 board_dimension=3,
                 block_number: int = 0,
                 block_positions: list = None,
                 winning_line_size=3,
                 d1=3,
                 d2=3,
                 t=20,
                 model_type=True,
                 play_mode=0,
                 p1_h_mode=None,
                 p2_h_mode=None,
                 recommend=False):
        if board_dimension not in range(3, 11):
            raise ValueError("Board dimension has to be between [3..10]")
        self._board_dimension = board_dimension
        if block_number not in range(0, 2 * board_dimension + 1):
            raise ValueError(f"Block number has to be between [0..{board_dimension * 2}]")
        self._block_number = block_number
        self._block_positions = block_positions
        if winning_line_size not in range(3, board_dimension + 1):
            raise ValueError("Winning line size can't be greater that board dimension")
        self.winning_line_size = winning_line_size
        if play_mode == 0:
            self.player_x = Player(self.HUMAN, d1, SimpleHeuristic() if p1_h_mode else ComplexHeuristic())
            self.player_o = Player(self.HUMAN, d2, SimpleHeuristic() if p2_h_mode else ComplexHeuristic())
        elif play_mode == 1:
            self.player_x = Player(self.HUMAN, d1, SimpleHeuristic() if p1_h_mode else ComplexHeuristic())
            self.player_o = Player(self.AI, d2, SimpleHeuristic() if p2_h_mode else ComplexHeuristic())
        elif play_mode == 2:
            self.player_x = Player(self.AI, d1, SimpleHeuristic() if p1_h_mode else ComplexHeuristic())
            self.player_o = Player(self.HUMAN, d2, SimpleHeuristic() if p2_h_mode else ComplexHeuristic())
        elif play_mode == 3:
            self.player_x = Player(self.AI, d1, SimpleHeuristic() if p1_h_mode else ComplexHeuristic())
            self.player_o = Player(self.AI, d2, SimpleHeuristic() if p2_h_mode else ComplexHeuristic())
        else:
            raise ValueError("No such mode available")
        self.recommend = recommend
        self.timeout = t
        self.player_turn = None
        self.current_state = []
        self.initialize_game()
        if model_type:
            self.search_algorithm = self.ALPHABETA
        else:
            self.search_algorithm = self.MINIMAX
        self.play(self.search_algorithm)

    def initialize_game(self):
        for i in range(self._board_dimension):
            self.current_state.append(['.'] * self._board_dimension)
        # X always starts
        self.player_turn = 'X'

    def add_blocks(self):
        if self._block_positions is None:
            self._block_positions = []
            while len(self._block_positions) < self._block_number:
                dimension = (random.randint(0, self._board_dimension - 1), random.randint(0, self._board_dimension - 1))
                if dimension not in self._block_positions:
                    self._block_positions.append(dimension)
        for coordinates in self._block_positions:
            self.current_state[coordinates[1]][coordinates[0]] = 'B'

    def draw_board(self):
        if self._block_number:
            self.add_blocks()
        print()
        print("Current board state:")
        for y in range(-1, len(self.current_state)):
            if y not in [-1, -2]:
                print(chr(65 + y), end="\t")
            elif y == -1:
                print(end="AZ#\t")
            for x in range(len(self.current_state)):
                if y not in [-1, -2]:
                    print(F'{self.current_state[y][x]}', end="\t")
                elif y == -1:
                    print(x, end="\t")
            print()

    # 'B' is for a block at that position
    def is_valid(self, px, py):
        try:
            if ord(px) not in range(65, 91) and ord(px) not in range(97, 123):
                return False
            if int(py) < 0 or int(py) >= self._board_dimension:
                return False
            elif self.current_state[ord(px) - 65 if ord(px) in range(65, 90) else ord(px) - 97][int(py)] != '.':
                return False
            elif self.current_state[ord(px) - 65 if ord(px) in range(65, 90) else ord(px) - 97][int(py)] == 'B':
                return False
            else:
                return True
        except ValueError:
            return False

    # Returns . if tie, X if X wins, 0 if 0 wins
    def is_end(self) -> str:
        winner = self.check_diagonal_board_win(self.current_state, self.winning_line_size)
        winner = self.check_horizontal_win(self.current_state, self.winning_line_size) if winner == None else winner
        winner = self.check_vertical_board_win(self.current_state, self.winning_line_size) if winner == None else winner
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
            entry = input(F'Player {self.player_turn}, enter your move:')
            try:
                split = entry.split(" ")
                if self.is_valid(split[0], split[1]):
                    return ord(split[0]) - 65 if ord(split[0]) in range(65, 90) else ord(split[0]) - 97, int(split[1])
                else:
                    print('The move is not valid! Try again.')
            except (ValueError, IndexError):
                print('The move is not valid! Try again.')

    def switch_player(self):
        if self.player_turn == 'X':
            self.player_turn = 'O'
        elif self.player_turn == 'O':
            self.player_turn = 'X'
        return self.player_turn

    def play(self, search_algorithm=None):
        while True:
            self.draw_board()
            if self.check_end():
                return
            start = time.time()
            if search_algorithm == self.MINIMAX:
                if self.player_turn == 'X':
                    (_, x, y) = self.minimax(max=False, start=start, depth=self.player_x.depth)
                else:
                    (_, x, y) = self.minimax(max=True, start=start, depth=self.player_o.depth)
            else:  # algo == self.ALPHABETA
                if self.player_turn == 'X':
                    (m, x, y) = self.alphabeta(max=False, start=start, depth=self.player_x.depth)
                else:
                    (m, x, y) = self.alphabeta(max=True, start=start, depth=self.player_o.depth)
            end = time.time()
            if (self.player_turn == 'X' and self.player_x.nature == self.HUMAN) or \
                    (self.player_turn == 'O' and self.player_o.nature == self.HUMAN):
                if self.recommend:
                    print(F'Evaluation time: {round(end - start, 7)}s')
                    print(F'Recommended move: x = {x}, y = {y}')
                (x, y) = self.input_move()
            if (self.player_turn == 'X' and self.player_x.nature == self.AI) or \
                    (self.player_turn == 'O' and self.player_o.nature == self.AI):
                print(F'Evaluation time: {round(end - start, 7)}s')
                print(F'Player {self.player_turn} under AI control plays: x = {x}, y = {y}')
            self.current_state[x][y] = self.player_turn
            self.switch_player()

    def minimax(self, depth, start, max=False):
        end = time.time()
        while True:
            # Minimizing for 'X' and maximizing for 'O'

            best_value = None
            best_x = None
            best_y = None

            for i in range(0, len(self.current_state)):
                for j in range(0, len(self.current_state)):
                    if end - start > self.timeout:
                        value = self.player_x.heuristic.calculate_value(self, max)
                        if best_value is None:
                            best_value = value
                            best_x = i
                            best_y = j
                        return best_value, best_x, best_y
                    if depth == 0 or self.is_end():
                        if max:
                            value = self.player_x.heuristic.calculate_value(self, max)
                            if best_value is None:
                                best_value = value
                                best_x = i
                                best_y = j
                            elif value > best_value:
                                best_value = value
                                best_x = i
                                best_y = j
                        else:
                            value = self.player_o.heuristic.calculate_value(self, max)
                            if best_value is None:
                                best_value = value
                                best_x = i
                                best_y = j
                            elif value < best_value:
                                best_value = value
                                best_x = i
                                best_y = j
                    else:
                        if self.current_state[i][j] == '.':
                            if max:
                                self.current_state[i][j] = 'O'
                                (v, _, _) = self.minimax(max=False, depth=depth - 1, start=start)
                                if best_value is None:
                                    best_value = v
                                    best_x = i
                                    best_y = j
                                elif v > best_value:
                                    best_value = v
                                    best_x = i
                                    best_y = j
                            else:
                                self.current_state[i][j] = 'X'
                                (v, _, _) = self.minimax(max=True, depth=depth - 1, start=start)

                                if best_value is None:
                                    best_value = v
                                    best_x = i
                                    best_y = j
                                elif v < best_value:
                                    best_value = v
                                    best_x = i
                                    best_y = j
                            self.current_state[i][j] = '.'
            return best_value, best_x, best_y


    def alphabeta(self, depth, start, alpha=-2, beta=2, max=False):
        # Minimizing for 'X' and maximizing for 'O'
        end=time.time()

        best_value = None
        best_x = None
        best_y = None

        for i in range(0, len(self.current_state)):
            for j in range(0, len(self.current_state)):
                if self.current_state[i][j] == '.':
                    if end - start > self.timeout:
                        value = self.player_x.heuristic.calculate_value(self, max)
                        if best_value is None:
                            best_value = value
                            best_x = i
                            best_y = j
                        return best_value, best_x, best_y
                    if depth == 0 or self.is_end():
                        if max:
                            value = self.player_x.heuristic.calculate_value(self, max)
                            if best_value is None:
                                best_value = value
                                best_x = i
                                best_y = j
                            elif value > best_value:
                                best_value = value
                                best_x = i
                                best_y = j
                        else:
                            value = self.player_o.heuristic.calculate_value(self, max)
                            if best_value is None:
                                best_value = value
                                best_x = i
                                best_y = j
                            elif value < best_value:
                                best_value = value
                                best_x = i
                                best_y = j
                    if max:
                        self.current_state[i][j] = 'O'
                        (v, _, _) = self.alphabeta(alpha, beta, max=False)

                        if best_value is None:
                            best_value = v
                            best_x = i
                            best_y = j
                        elif v > best_value:
                            best_value = v
                            best_x = i
                            best_y = j
                    else:
                        self.current_state[i][j] = 'X'
                        (v, _, _) = self.alphabeta(alpha, beta, max=True)

                        if best_value is None:
                            best_value = v
                            best_x = i
                            best_y = j
                        elif v < best_value:
                            best_value = v
                            best_x = i
                            best_y = j
                    self.current_state[i][j] = '.'

                    if max:
                        if best_value is None:
                            best_value = v
                            best_x = i
                            best_y = j
                        if best_value >= beta:
                            return best_value, best_x, best_y
                        if best_value > alpha:
                            alpha = best_value
                    else:
                        if best_value is None:
                            best_value = v
                            best_x = i
                            best_y = j
                        if best_value <= alpha:
                            return best_value, best_x, best_y
                        if best_value < beta:
                            beta = best_value

        return best_value, best_x, best_y

    @staticmethod
    def check_diagonal_board_win(board, success_factor):
        length = len(board)
        x_expected_winning_criteria = 'X' * success_factor
        o_expected_winning_criteria = 'O' * success_factor
        for column in range(1, length):
            target_diagonal = ''
            for row, row_list in enumerate(board):
                if 0 <= column + row < length:
                    target_diagonal += row_list[column + row]
            if len(target_diagonal) >= success_factor:
                if x_expected_winning_criteria in target_diagonal:
                    return 'X'
                elif o_expected_winning_criteria in target_diagonal:
                    return 'O'
        for column in reversed(range(-(length - 1), 1)):
            target_diagonal = ''
            for row, row_list in enumerate(board):
                if 0 <= column + row < length:
                    target_diagonal += row_list[column + row]
            if len(target_diagonal) >= success_factor:
                if x_expected_winning_criteria in target_diagonal:
                    return 'X'
                elif o_expected_winning_criteria in target_diagonal:
                    return 'O'
        for column in reversed(range(length)):
            target_diagonal = ''
            for row, row_list in enumerate(board):
                if 0 <= column - row < length:
                    target_diagonal += row_list[column - row]
            if len(target_diagonal) >= success_factor:
                if x_expected_winning_criteria in target_diagonal:
                    return 'X'
                elif o_expected_winning_criteria in target_diagonal:
                    return 'O'
        for column in range(1, length):
            target_diagonal = ''
            for row, row_list in enumerate(reversed(board)):
                if 0 <= column + row < length:
                    target_diagonal += row_list[column + row]
            if len(target_diagonal) >= success_factor:
                if x_expected_winning_criteria in target_diagonal:
                    return 'X'
                elif o_expected_winning_criteria in target_diagonal:
                    return 'O'

    @staticmethod
    def check_vertical_board_win(board, success_factor) -> str:
        x_expected_winning_criteria = 'X' * success_factor
        o_expected_winning_criteria = 'O' * success_factor
        for column in range(len(board)):
            target_column = ''
            for row_list in board:
                target_column += row_list[column]
            if x_expected_winning_criteria in target_column:
                return 'X'
            elif o_expected_winning_criteria in target_column:
                return 'O'

    @staticmethod
    def check_horizontal_win(board, success_factor) -> str:
        x_expected_winning_criteria = 'X' * success_factor
        o_expected_winning_criteria = 'O' * success_factor
        for row in range(len(board)):
            target_row = ''.join(board[row])
            if x_expected_winning_criteria in target_row:
                return 'X'
            elif o_expected_winning_criteria in target_row:
                return 'O'


# XXX: Maybe encapsulate parameter choice in function
def try_int(user_input):
    try:
        return int(user_input)
    except ValueError:
        print("Please, enter an integer value!")
        return None


def try_ord(user_input):
    try:
        return ord(user_input)
    except ValueError:
        print("Please, enter a single character!")
        return None


def input_block_positions(number_of_blocks, board_dimensions):
    demo_board = []
    row = []
    blocks_positions = []
    for i in range(1, board_dimensions * board_dimensions + 1):
        row.append(i)
        if len(row) >= board_dimensions:
            demo_board.append(tuple(row))
            row = []
    block_position = None
    while block_position is None \
            or (block_position if block_position is not None else board_dimensions + 1) > board_dimensions * board_dimensions + 1 \
            or len(blocks_positions) < number_of_blocks:
        for row in demo_board:
            print(row)
        block_position = try_int(input(f"Please, choose the block positions for block number {len(blocks_positions) + 1} from the board:"))
        for row in demo_board:
            if block_position in row:
                position = (demo_board.index(row), row.index(block_position))
                if position not in blocks_positions:
                    blocks_positions.append(position)
    print(blocks_positions)
    return blocks_positions


def main():
    print("Choose your game parameters")
    board_dimension = None
    while board_dimension is None:
        board_dimension = try_int(input("Enter board size: "))
    block_number = None
    while block_number is None:
        block_number = try_int(input("Enter the number of blocks: "))

    if block_number != 0:
        random_approval = None
        random_blocks_positions_answer = input("Do you wish to have randomize blocks positions (y/N)? ")
        if random_blocks_positions_answer.lower() == "y":
            random_approval = True
        elif random_blocks_positions_answer.lower() == "n":
            random_approval = False

        block_positions = None
        if not random_approval:
            block_positions = input_block_positions(block_number, board_dimension)

    winning_line_size = None
    while not winning_line_size:
        winning_line_size = try_int(input("Enter the winning line size: "))

    print("Play modes:")
    print("H-H: 0")
    print("H-AI: 1")
    print("AI-H: 2")
    print("AI-AI: 3")
    play_mode = None
    while play_mode is None or 0 > play_mode > 3:
        play_mode = try_int(input("Enter the play mode (0-3): "))

    recommend = False
    if play_mode < 3:
        recommend_answer = input("Do you wish to get move recommendations (y/n)? ")
        if recommend_answer.lower() == "y":
            recommend = True
        elif recommend_answer.lower() == "n":
            recommend = False

    if not recommend and play_mode == 0:
        print("Game initialized!")
        g = Game(
            board_dimension=board_dimension,
            block_number=block_number,
            winning_line_size=winning_line_size,
            play_mode=play_mode,
            recommend=recommend
        )

    # # TODO: If  there is time, add removing recommendation for play_mode = 1 & 2
    else:
        d1 = try_int(input("Enter search depth for player 1 (AI): "))
        d2 = try_int(input("Enter search depth for player 2 (AI): "))

        timeout = try_int(input("Enter search algorithm timeout: "))

        model_type_answer = input("Do you wish to use an alpha-beta search (y/n)? ")
        model_type = True
        if model_type_answer.lower() == "y":
            model_type = True
        elif model_type_answer.lower() == "n":
            model_type = False

        h_type_answer = input("Do you wish to use a simple heuristic for player 1 (y/n)? ")
        p1_h_mode = True
        if h_type_answer.lower() == "y":
            p1_h_mode = True
        elif h_type_answer.lower() == "n":
            p1_h_mode = False

        h_type_answer = input("Do you wish to use a simple heuristic for player 2 (y/n)? ")
        p2_h_mode = True
        if h_type_answer.lower() == "y":
            p2_h_mode = True
        elif h_type_answer.lower() == "n":
            p2_h_mode = False

        # Outputting to a text file.
        file_name = "gameTrace-" + str(board_dimension) + str(block_number) + str(winning_line_size) + str(timeout) + ".txt"
        file = open(file_name, "w+")
        board_parameters = "n=" + str(board_dimension) + " b=" + str(block_number) + " s=" + str(winning_line_size) + " t=" + str(timeout)
        file.write(board_parameters)
        if block_number > 0:
            file.write("\n" + str(block_positions))

        print()
        print("Game initialized!")
        print()
        # TODO: Add block_positions here block number > 1
        g = Game(
            board_dimension=board_dimension,
            block_number=block_number,
            winning_line_size=winning_line_size,
            play_mode=play_mode,
            d1=d1,
            d2=d2,
            t=timeout,
            model_type=model_type,
            p1_h_mode=p1_h_mode,
            p2_h_mode=p1_h_mode,
            recommend=recommend
        )

    # # closing the file.
    # file.close()


if __name__ == "__main__":
    main()
