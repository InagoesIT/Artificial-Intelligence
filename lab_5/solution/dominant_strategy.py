from solution.contract import Solution


class DominantStrategy(Solution):
    def __init__(self, strategies, model):
        self.strategies = strategies
        self.model = model

    def pretty_print(self):
        for player_index in self.strategies:
            strategies_size = len(self.strategies[player_index])
            if strategies_size == 0:
                print(f"The player {self.model.players[player_index]} has no dominant strategies.")
            else:
                strategies_names = list(map((lambda index: self.model.strategy_names[player_index][index]), self.strategies[player_index]))
                if strategies_size == 1:
                    print(f"The dominant strategy found for the player {self.model.players[player_index]} is: {strategies_names[0]}")
                else:
                    print(f"The dominant strategies found for the player {self.model.players[player_index]} are: {strategies_names}")
