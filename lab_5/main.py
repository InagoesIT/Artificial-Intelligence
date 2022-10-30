import os

from problem.parser import Parser
from solver.algorithm import Algorithm

if __name__ == '__main__':
    parser = Parser(os.path.join(".", "input", "data.txt"))
    model = parser.parse_data_into_model()
    model.pretty_print()
    algorithm = Algorithm(model)
    solution = algorithm.get_nash_equilibria_states()
    solution.pretty_print()
