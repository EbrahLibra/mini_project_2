import abc


# Abstract class
class BaseHeuristic(abc.ABC):

    def __init__(self, board):
        self._board = board

    @abc.abstractmethod
    def calculate_value(self) -> int:
        pass
