import random
from base_heuristic import BaseHeuristic


class SimpleHeuristic(BaseHeuristic):
    def __init__(self, board, max=False):
        super().__init__(board)
        self._max = max
        self._board_size = len(board)

    # TODO This function is not working properly
    # We need better solution
    def calculate_value(self) -> int:
        if max:
            return -random.randint(0, self._board_size - 1)
        else:
            return +random.randint(0, self._board_size - 1)
