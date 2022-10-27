import argparse
import logging

from algorithm import Algorithm

logging.basicConfig(filename='results.log', level=logging.INFO)


class ProblemModel:
    def __init__(self, n: int, blocks: list):
        self.n = n
        self.queen_domains = [{domain_value for domain_value in range(n)} for _ in range(n)]
        for block in blocks:
            self.queen_domains[block[0]].remove(block[1])
        self.queen_column = [-1 for _ in range(n)]

    def pretty_print_model(self):
        for index, domain in enumerate(self.queen_domains):
            logging.info(f"Domain of queen with {index} is {domain}")
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
    algorithm.run()


if __name__ == "__main__":
    main()
