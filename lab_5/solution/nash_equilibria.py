from solution.contract import Solution


class NashSolution(Solution):
    def __init__(self, equilibrias):
        self.equilibrias = equilibrias

    def pretty_print(self):
        for eq in self.equilibrias:
            print(f"Nash equilibria found on {eq}")
