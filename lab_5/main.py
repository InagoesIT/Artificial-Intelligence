import glob
import os

from problem.parser import Parser
from solver.dominant_strategy import DominantStrategyAlgorithm
from solver.nash_equilibria import NashAlgorithm

if __name__ == '__main__':
    for file_name in glob.glob(os.path.join('.', 'input', '*.txt')):
        print(f"The result for parsing the file {file_name} is:")
        parser = Parser(file_name)
        model = parser.parse_data_into_model()
        model.pretty_print()
        algorithm = NashAlgorithm(model)
        solution = algorithm.run()
        solution.pretty_print()
        print()

        algorithm = DominantStrategyAlgorithm(model)
        solution = algorithm.run()
        solution.pretty_print()
        print("=" * 100)
        print()
