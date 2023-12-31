import argparse
import logging
import sys

from algorithm import Algorithm

TEST_FAILED__NOOB = "Test failed for pair ({}, {}) ({}, {}). Noob"

logging.basicConfig(filename='results.log', level=logging.INFO)


class ProblemModel:
    def __init__(self, n: int, blocks: list):
        self.n = n
        self.queen_domains = [{domain_value for domain_value in range(n)} for _ in range(n)]
        for block in blocks:
            self.queen_domains[block[0]].remove(block[1])
        self.queen_column = [-1 for _ in range(n)]
        self.is_model_good = True

    def pretty_print_model(self, debug_mode=False):
        if debug_mode:
            for index, domain in enumerate(self.queen_domains):
                logging.info(f"Domain of queen with {index} is {domain}")

        for index, column in enumerate(self.queen_column):
            for index1, column1 in enumerate(self.queen_column):
                if index == index1:
                    continue
                if abs(index - index1) == abs(column - column1):
                    logging.error(TEST_FAILED__NOOB.format(index, column, index1, column1))
                    self.is_model_good = False
                    return
                if column == column1:
                    logging.error(TEST_FAILED__NOOB.format(index, column, index1, column1))
                    self.is_model_good = False
                    return

        if debug_mode:
            matrix = [[None] * self.n for _ in range(self.n)]
            for index, column in enumerate(self.queen_column):
                matrix[index][column] = 'xx'
            for line in matrix:
                logging.info(f"{line}")

        for index, column in enumerate(self.queen_column):
            logging.info(f"Queen with index {index} placed on column {column}")


def main():
    parser = argparse.ArgumentParser(description='N queens problem')
    required_parser = parser.add_argument_group(
        'required named arguments')
    required_parser.add_argument('-n', '--number-queens', type=int, help='Number of queens',
                                 required=True)
    parser.add_argument('-b', '--blocks', nargs='*', type=int, help='Block pairs', required=False, action='append')
    args = vars(parser.parse_args())
    model = ProblemModel(args["number_queens"], args["blocks"])
    algorithm = Algorithm(model)
    sys.exit(algorithm.run())


if __name__ == "__main__":
    main()
