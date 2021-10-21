import abc

# Abstract class
class BaseHeuristic(abc.ABC):

    @abc.abstractmethod
    def calculate_value(self) -> int:
        pass