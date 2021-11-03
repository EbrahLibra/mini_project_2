import time
from simple_heuristic import SimpleHeuristic
from complex_heuristic import ComplexHeuristic
from search_algorithm import SearchAlgorithm



class Game:
    HUMAN = 0
    AI = 1

    # TODO: Randomize block positions (use functions, which is called in init)
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
        if winning_line_size > board_dimension:
            raise ValueError("Winning line size can't be greater that board dimension")
        self._board_dimension = board_dimension
        self._block_number = block_number

        self._block_positions = block_positions
        self._winning_line_size = winning_line_size
        self._play_mode = play_mode
        self.recommend = recommend
        self.player_turn = None
        self.current_state = []
        self.initialize_game()
        self._search_algo = self.initialize_search_algorithm(
            d1=d1,
            d2=d2,
            t=t,
            model_type=model_type,
            p1_h_mode=p1_h_mode,
            p2_h_mode=p2_h_mode
        )

    def initialize_game(self):
        for i in range(self._board_dimension):
            self.current_state.append(['.'] * self._board_dimension)

        # X always starts
        self.player_turn = 'X'

    def initialize_search_algorithm(self,
                                    d1: int,
                                    d2: int,
                                    t: int,
                                    model_type: bool,
                                    p1_h_mode: bool,
                                    p2_h_mode: bool):
        if p1_h_mode:
            e1 = SimpleHeuristic()
        else:
            e1 = ComplexHeuristic(self._winning_line_size)
        if p2_h_mode:
            e2 = SimpleHeuristic()
        else:
            e2 = ComplexHeuristic(self._winning_line_size)

        search_algo = SearchAlgorithm(
            e1=e1,
            e2=e2,
            d1=d1,
            d2=d2,
            t=t,
            model_type=model_type,
        )
        return search_algo

    def add_blocks(self):
        for coordinates in self._block_positions:
            self.current_state[coordinates[0]][coordinates[1]] = 'B'

    def draw_board(self):
        if self._block_positions is not None:
            self.add_blocks()
        print()
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

    # TODO: Implement _play_mode functionality
    # XXX: Uncomment when AI added components
    def play(self,
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
            #     (m, x, y) = self._search_algo.evaluate(game=self, max=True)
            # else:
            #     (m, x, y) = self._search_algo.evaluate(game=self, max=False)
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
# TODO: Check for correct in input

def main():
    print("Choose your game parameters")

    board_dimension = int(input("Enter board size: "))
    block_number = int(input("Enter the number of blocks: "))
    winning_line_size = int(input("Enter the winning line size: "))

    print("Play modes:")
    print("H-H: 0")
    print("H-AI: 1")
    print("AI-H: 2")
    print("AI-AI: 3")
    play_mode = int(input("Enter the play mode (0-3): "))

    recommend = False
    if play_mode < 3:
        recommend_answer = input("Do you wish to get move recommendations (y/N)? ")
        if recommend_answer.lower() == "y":
            recommend = True
        elif recommend_answer.lower() == "n":
            recommend = False

    if not recommend and play_mode == 0:
        g = Game(
            board_dimension=board_dimension,
            block_number=block_number,
            winning_line_size=winning_line_size,
            play_mode=play_mode,
            recommend=recommend
        )
        g.play()

    # TODO: If  there is time, add removing recommendation for play_mode = 1 & 2
    else:
        d1 = int(input("Enter search depth for player 1 (AI): "))
        d2 = int(input("Enter search depth for player 2 (AI): "))

        t = int(input("Enter search algorithm timeout: "))

        model_type_answer = input("Do you wish to use an alpha-beta search (y/N)? ")
        model_type = True
        if model_type_answer.lower() == "y":
            model_type = True
        elif model_type_answer.lower() == "n":
            model_type = False

        h_type_answer = input("Do you wish to use a simple heuristic for player 1 (y/N)? ")
        p1_h_mode = True
        if h_type_answer.lower() == "y":
            p1_h_mode = True
        elif h_type_answer.lower() == "n":
            p1_h_mode = False

        h_type_answer = input("Do you wish to use a simple heuristic for player 2 (y/N)? ")
        p2_h_mode = True
        if h_type_answer.lower() == "y":
            p2_h_mode = True
        elif h_type_answer.lower() == "n":
            p2_h_mode = False

        g = Game(
            board_dimension=board_dimension,
            block_number=block_number,
            winning_line_size=winning_line_size,
            play_mode=play_mode,
            d1=d1,
            d2=d2,
            t=t,
            model_type=model_type,
            p1_h_mode=p1_h_mode,
            p2_h_mode=p2_h_mode,
            recommend=recommend
        )
        g.play()


if __name__ == "__main__":
    main()
