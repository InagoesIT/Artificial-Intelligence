from solution.nash_equilibria import NashSolution
from solver.contract import Algorithm


class NashAlgorithm(Algorithm):
    def __init__(self, model) -> None:
        super().__init__(model)
        self.best_moves = [[[False, False] for _ in range(self.model.m)]
                           for _ in range(self.model.n)
                           ]
        self.n = self.model.n
        self.m = self.model.m

    def get_best_choices(self, max_key, max_value, player):
        return_dict = {x: list() for x in range(max_key)}

        for key in range(max_key):
            current_best = -1
            for line in range(max_value):
                current_value = self.model.values[line][key][player]
                if current_value > current_best:
                    current_best = current_value
                    return_dict[key] = [line]
                elif current_best == current_value:
                    return_dict[key].append(line)
        return return_dict

    def mark_best_states(self, choices, player):
        for item in choices.items():
            for value in item[1]:
                if player == 0:
                    self.best_moves[value][item[0]][player] = True
                else:
                    self.best_moves[item[0]][value][player] = True

    def run(self) -> NashSolution:
        first_player_choices = self.get_best_choices(self.m, self.n, 0)
        second_player_choices = self.get_best_choices(self.n, self.m, 1)

        self.mark_best_states(first_player_choices, 0)
        self.mark_best_states(second_player_choices, 1)

        nash_equilibrias = []
        for line in range(self.n):
            for column in range(self.m):
                if self.best_moves[line][column] == [True, True]:
                    nash_equilibrias.append((line, column))
        return NashSolution(nash_equilibrias)
