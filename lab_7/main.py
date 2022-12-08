import random
from collections import defaultdict

from algorithm import Algorithm


def main():
    algorithm = Algorithm(n=4, m=12, discount=0.9,
                          learning_rate=0.1)
    algorithm.set_playground()
    algorithm.run()
    algorithm.pretty_print_stats()

if __name__ == '__main__':
    main()
