import abc


# Abstract class
class BaseHeuristic(abc.ABC):
    @abc.abstractmethod
    def calculate_value(self, game, max_turn) -> int:
        pass
