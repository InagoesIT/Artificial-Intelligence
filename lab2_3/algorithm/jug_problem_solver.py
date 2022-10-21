import logging
import argparse
from bfs import BfsAlgorithm
from bkt import BktAlgorithm
from hill_climbing import HillClimbingAlgorithm
from a_star import AStarAlgorithm
from model import ProblemModel

logging.basicConfig(filename='../lab2_3/logging/ai.log', level=logging.INFO)

algorithm_mapper = {
    'bkt': BktAlgorithm,
    'bfs': BfsAlgorithm,
    'hill': HillClimbingAlgorithm,
    'astar': AStarAlgorithm
}


def main():
    parser = argparse.ArgumentParser(description='Jug Problem Menu')
    required_parser = parser.add_argument_group(
        'required named arguments')
    required_parser.add_argument('-n', type=int, help='first jug capacity',
                                 required=True)
    required_parser.add_argument('-m', type=int, help='second jug capacity', required=True)
    required_parser.add_argument('-k', type=int, help='desired amount', required=True)
    parser.add_argument('-a',
                        '--algorithm', metavar='A', choices=['bkt', 'bfs', 'astar', 'hill'],
                        help='algorithm to be applied to the instance of the problem: %(choices)s, default: %(default)s',
                        required=False, default='bfs')

    args = vars(parser.parse_args())
    algorithm_class = algorithm_mapper[args['algorithm']]
    model = ProblemModel(n=args['n'], m=args['m'], k=args['k'])
    algorithm = algorithm_class(model=model)
    algorithm.run()
    if algorithm.solution_found:
        print("Solution found. Check logs")
        algorithm.pretty_print_solution()
    else:
        print("No solution found")

    logging.info("\n")


if __name__ == "__main__":
    main()
