import time
from search_algorithm import SearchAlgorithm
from simple_heuristic import SimpleHeuristic
from complex_heuristic import ComplexHeuristic
from base_heuristic import BaseHeuristic

class Game:

    # Parameters that still need to be added:
    # - the maximum depth of the adversarial search for player 1 and for player 2 (d1, d2)
    # - the maximum allowed time (in seconds) for your program to return a move (t)
    # - a Boolean to force the use of either minimax (FALSE) or alphabeta (TRUE) (a)
    # - the play modes - H-H, H-AI, AI-H and AI-AI (pm)
    def __init__(self,
                 board_dimension: int,
                 block_number: int,
                 block_positions: [(int, int)],
                 winning_line_size: int):
        self._board_dimension = board_dimension
        self._block_number = block_number
        self._block_position = block_positions
        self._winning_line_size = winning_line_size
        self.player_turn = None
        self.current_state = []
        self.initialize_game()

    def initialize_game(self):
        for i in range(self._board_dimension):
            self.current_state.append(['.'] * self._board_dimension)

        # X always starts
        self.player_turn = 'X'

    def draw_board(self):
        print()
        print("Current board state:")
        for y in range(self._board_dimension):
            for x in range(self._board_dimension):
                print(F'{self.current_state[x][y]}', end="")
            print()
        print()

    # 'B' is for a block at that position
    def is_valid(self, px, py):
        if px < 0 or px > self._board_dimension or py < 0 or py > self._board_dimension:
            return False
        elif self.current_state[px][py] != '.':
            return False
        elif self.current_state[px][py] != 'B':
            return False
        else:
            return True

    # TODO: Check end conditions
    # Check skeleton-tictactoe method
    # Returns . if tie, X if X wins, 0 if 0 wins
    def is_end(self) -> str:
        return ''

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
            px = int(input('enter the x coordinate: '))
            py = int(input('enter the y coordinate: '))
            if self.is_valid(px, py):
                return (px, py)
            else:
                print('The move is not valid! Try again.')

    def switch_player(self):
        if self.player_turn == 'X':
            self.player_turn = 'O'
        elif self.player_turn == 'O':
            self.player_turn = 'X'
        return self.player_turn

    # TODO: Implement play loop
    def play(self,
             algo: SearchAlgorithm,
             e1: BaseHeuristic,
             e2: BaseHeuristic,
             player_x=None,
             player_o=None):
        pass

def main():
    g = Game(5, 0, [], 3)
    g.play()

if __name__ == "__main__":
    main()
