import random
from base_heuristic import BaseHeuristic


class SimpleHeuristic(BaseHeuristic):
    def __init__(self):
        pass

    # TODO This function is not working properly
    # We need better solution
    def calculate_value(self, success_factor, max_turn=False) -> int:
        if max_turn:
            return -(success_factor-1)
        else:
            return success_factor-1
