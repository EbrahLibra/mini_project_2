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
        self._e1 = e1
        self._e2 = e2

    def evaluate(self, max: bool, game):
        if self.model == self.MINIMAX:
            return self._evaluate_minimax(max, game)
        else:
            return self._evaluate_alpha_beta(max, game)

    # TODO: return (value, x, y) of optimal position using euristics
    # XXX: Not tested yet (based on skeleton-tictactoe)
    def _evaluate_minimax(self, max: bool, game):
        value = 2
        if max:
            value = -2
        x = None
        y = None
        result = game.is_end()
        if result == 'X':
            return (-1, x, y)
        elif result == 'O':
            return (1, x, y)
        elif result == '.':
            return (0, x, y)
        for i in range(0, len(game.current_state)):
            for j in range(0, len(game.current_state)):
                if game.current_state[i][j] == '.':
                    if max:
                        game.current_state[i][j] = 'O'
                        (v, _, _) = self._evaluate_minimax(max=False, game=game)
                        if v > value:
                            value = v
                            x = i
                            y = j
                    else:
                        game.current_state[i][j] = 'X'
                        (v, _, _) = self._evaluate_minimax(max=True, game=game)
                        if v < value:
                            value = v
                            x = i
                            y = j
                    game.current_state[i][j] = '.'
        return (value, x, y)

    # TODO: return (value, x, y) of optimal position using euristics
    # XXX: Not tested yet (based on skeleton-tictactoe)
    def _evaluate_alpha_beta(self, max: bool, game, alpha=-2, beta=2):
        value = 2
        if max:
            value = -2
        x = None
        y = None
        result = game.is_end()
        if result == 'X':
            return (-1, x, y)
        elif result == 'O':
            return (1, x, y)
        elif result == '.':
            return (0, x, y)
        for i in range(0, len(game.current_state)):
            for j in range(0, len(game.current_state)):
                if game.current_state[i][j] == '.':
                    if max:
                        game.current_state[i][j] = 'O'
                        (v, _, _) = self._e1.calculate_value(game.current_state)
                        if v > value:
                            value = v
                            x = i
                            y = j
                    else:
                        game.current_state[i][j] = 'X'
                        (v, _, _) = self._e1.calculate_value(game.current_state)
                        if v < value:
                            value = v
                            x = i
                            y = j
                    game.current_state[i][j] = '.'
                    if max:
                        if value >= beta:
                            return (value, x, y)
                        if value > alpha:
                            alpha = value
                    else:
                        if value <= alpha:
                            return (value, x, y)
                        if value < beta:
                            beta = value
        return (value, x, y)

