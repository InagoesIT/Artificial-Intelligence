import os

from problem.parser import Parser
from solver.nash_algorithm import NashAlgorithm

if __name__ == '__main__':
    parser = Parser(os.path.join(".", "input", "data.txt"))
    model = parser.parse_data_into_model()
    model.pretty_print()
    algorithm = NashAlgorithm(model)
    solution = algorithm.run()
    solution.pretty_print()
