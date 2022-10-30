from solution.contract import NashSolution
from solver.contract import Algorithm


class NashAlgorithm(Algorithm):
    def __init__(self, model) -> None:
        super().__init__(model)
        self.best_moves = [[[False, False] for _ in range(self.model.m)]
                           for _ in range(self.model.n)
                           ]
        self.n = len(self.model.row_names)
        self.m = len(self.model.column_names)

    def run(self) -> NashSolution:
        first_player_choices = dict()
        for column in range(self.m):
            current_best = -1
            for line in range(self.n):
                current_value = self.model.values[line][column][0]
                if current_value > current_best:
                    first_player_choices[column] = [line]
                elif current_best == current_value:
                    first_player_choices[column].append(line)

        second_player_choices = dict()
        for line in range(self.n):
            current_best = -1
            for column in range(self.m):
                current_value = self.model.values[line][column][1]
                if current_value > current_best:
                    second_player_choices[line] = [column]
                elif current_best == current_value:
                    second_player_choices[line].append(column)

        for item in first_player_choices.items():
            for line in item[1]:
                self.best_moves[line][item[0]][0] = True

        for item in second_player_choices.items():
            for column in item[1]:
                self.best_moves[item[0]][column][1] = True

        nash_equilibrias = []
        for line in range(self.n):
            for column in range(self.m):
                if self.best_moves[line][column] == [True, True]:
                    nash_equilibrias.append((line, column))
        return NashSolution(nash_equilibrias)
