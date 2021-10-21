from base_heuristic import BaseHeuristic

class SearchAlgorithm:
    MINIMAX = 0
    ALPHABETA = 1

    def __init__(self,
                 model: int,
                 e1: BaseHeuristic,
                 e2: BaseHeuristic):
        if model == 0:
            self.model = self.MINIMAX
        elif model == 1:
            self.model = self.ALPHABETA
        else:
            self.model = self.MINIMAX

    def evaluate(self):
        if self.model == self.MINIMAX:
            return self._evaluate_minimax()
        else:
            return self._evaluate_alpha_beta()

    # TODO: return (value, x, y) of optimal position using euristics
    def _evaluate_minimax(self):
        pass

    # TODO: return (value, x, y) of optimal position using euristics
    def _evaluate_alpha_beta(self):
        pass
