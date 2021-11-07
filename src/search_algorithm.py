from base_heuristic import BaseHeuristic


class SearchAlgorithm:
    MINIMAX = 0
    ALPHABETA = 1

    def __init__(self,
                 e1: BaseHeuristic,
                 e2: BaseHeuristic,
                 d1: int,
                 d2: int,
                 t: int,
                 model_type: bool,
                 ):
        self._model_type = model_type
        self._e1 = e1
        self._e2 = e2
        self._d1 = d1
        self._d2 = d2
        self._t = t

    def evaluate(self, max: bool, game):
        eval_game = game
        if not self._model_type:
            if max:
                return self._evaluate_minimax(max,
                                              eval_game,
                                              depth=self._d1,
                                              estimation_function=self._e1)
            else:
                return self._evaluate_minimax(max,
                                              eval_game,
                                              depth=self._d2,
                                              estimation_function=self._e2)
        else:
            if max:
                return self._evaluate_alpha_beta(max,
                                                 eval_game,
                                                 depth=self._d1,
                                                 estimation_function=self._e1)
            else:
                return self._evaluate_alpha_beta(max,
                                                 eval_game,
                                                 depth=self._d2,
                                                 estimation_function=self._e2)

    # TODO: return (value, x, y) of optimal position using heuristics
    # TODO: Implement search depth
    # XXX: Not tested yet (based on skeleton-tictactoe)
    def _evaluate_minimax(self, max: bool, game, depth, estimation_function):

        value = estimation_function.calculate_value(
            game=game,
            max_turn=max
        )

        if depth == 0:
            return (value, None, None)

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
                        (v, _, _) = self._evaluate_minimax(max=False,
                                                           game=game,
                                                           depth=depth-1,
                                                           estimation_function=estimation_function)
                        if v > value:
                            value = v
                            x = i
                            y = j
                    else:
                        game.current_state[i][j] = 'X'
                        (v, _, _) = self._evaluate_minimax(max=True,
                                                           game=game,
                                                           depth=depth-1,
                                                           estimation_function=estimation_function)
                        if v < value:
                            value = v
                            x = i
                            y = j
                    game.current_state[i][j] = '.'
        return (value, x, y)

    # TODO: return (value, x, y) of optimal position using heuristics
    # TODO: Implement search depth & estimation function
    # XXX: Not tested yet (based on skeleton-tictactoe)
    def _evaluate_alpha_beta(self, max: bool, game, depth, estimation_function, alpha=-2, beta=2):

        value = estimation_function.calculate_value(
            game=game,
            max_turn=max
        )

        if depth == 0:
            return (value, None, None)

        x = None
        y = None

        result = game.is_end()
        # TODO: Find winning value that makes sense (
        #  maybe normalize heuristics to return values between -1 and 1)
        if result == 'X':
            return (-10000, x, y)
        elif result == 'O':
            return (10000, x, y)
        elif result == '.':
            return (0, x, y)

        for i in range(0, len(game.current_state)):
            for j in range(0, len(game.current_state)):
                if game.current_state[i][j] == '.':
                    if max:
                        game.current_state[i][j] = 'O'
                        (v, _, _) = self._evaluate_alpha_beta(max=False,
                                                              game=game,
                                                              depth=depth-1,
                                                              estimation_function=estimation_function)
                        if v > value:
                            value = v
                            x = i
                            y = j
                    else:
                        game.current_state[i][j] = 'X'
                        (v, _, _) = self._evaluate_alpha_beta(max=True,
                                                              game=game,
                                                              depth=depth-1,
                                                              estimation_function=estimation_function)
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

