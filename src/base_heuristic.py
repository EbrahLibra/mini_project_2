import abc


# Abstract class
class BaseHeuristic(abc.ABC):
    @abc.abstractmethod
    def calculate_value(self, board, max_turn=False) -> int:
        pass
