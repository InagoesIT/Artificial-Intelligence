from solution.dominant_strategy import DominantStrategy
from solver.contract import Algorithm


class DominantStrategyAlgorithm(Algorithm):
    def __init__(self, model) -> None:
        super().__init__(model)
        self.row_nr = self.model.n
        self.column_nr = self.model.m

    def get_best_strategies_for(self, player, player_strategies_nr, opponent_strategies_nr):
        best_strategies = {index: [0] for index in range(opponent_strategies_nr)}

        for opponent_strategy_index in range(opponent_strategies_nr):
            for player_strategy_index in range(1, player_strategies_nr):
                if player == 0:
                    reward_player = self.model.values[player_strategy_index][opponent_strategy_index][player]
                    best_strategy_index = best_strategies[opponent_strategy_index][0]
                    best_strategy_reward = self.model.values[best_strategy_index][opponent_strategy_index][player]
                else:
                    reward_player = self.model.values[opponent_strategy_index][player_strategy_index][player]
                    best_strategy_index = best_strategies[opponent_strategy_index][0]
                    best_strategy_reward = self.model.values[opponent_strategy_index][best_strategy_index][player]

                if best_strategy_reward < reward_player:
                    best_strategies[opponent_strategy_index] = [player_strategy_index]
                elif best_strategy_reward == reward_player:
                    best_strategies[opponent_strategy_index].append(player_strategy_index)

        return best_strategies

    @staticmethod
    def get_dominant_strategies_for(best_strategies: dict):
        best_strategies_sets = [set(player_strategies) for player_strategies in best_strategies.values()]
        common_strategies = set()

        for index in range(0, len(best_strategies_sets) - 1, 2):
            common_strategies = best_strategies_sets[index].intersection(best_strategies_sets[index + 1])
            if len(common_strategies) == 0:
                return []

        return common_strategies

    def run(self):
        best_strategies_first_player = self.get_best_strategies_for(player=0, player_strategies_nr=self.row_nr,
                                                                    opponent_strategies_nr=self.column_nr)
        dominant_strategies_first_player = self.get_dominant_strategies_for(best_strategies=best_strategies_first_player)

        best_strategies_second_player = self.get_best_strategies_for(player=1, player_strategies_nr=self.column_nr,
                                                                     opponent_strategies_nr=self.row_nr)
        dominant_strategies_second_player = self.get_dominant_strategies_for(best_strategies=best_strategies_second_player)

        result = {0: dominant_strategies_first_player, 1: dominant_strategies_second_player}
        return DominantStrategy(result, self.model)
