import logging
import random


class Tester:
    def __init__(self, max_n, max_m, max_k, model_class, algorithm_class):
        self.max_n = max_n
        self.max_m = max_m
        self.max_k = max_k
        self.model_class = model_class
        self.algorithm_class = algorithm_class
        self.passed_tests = 0
        self.failed_tests = 0

    @staticmethod
    def gcd(a, b):
        while b != 0:
            r = a % b
            a = b
            b = r
        return a

    def run_test(self):
        actual_n = random.randint(1, self.max_n)
        actual_m = random.randint(1, self.max_m)
        actual_k = random.randint(1, min(actual_n, actual_m))
        must_pass = False
        if actual_k % Tester.gcd(actual_n, actual_m) == 0:
            must_pass = True

        model = self.model_class(n=actual_n, m=actual_m, k=actual_k)
        algorithm = self.algorithm_class(model=model)
        algorithm.run()

        logging.info("Actual n: %d actual m: %d actual k: %d and must pass: %s" %
                     (actual_n, actual_m, actual_k, must_pass))
        logging.info("Solution found: %s\n" % algorithm.solution_found)
        if must_pass == algorithm.solution_found:
            self.passed_tests += 1
        else:
            self.failed_tests += 1

    def pretty_print_final_results(self):
        logging.info("From %d tests %d passed and %d failed\n\n\n\n" %
                     (self.passed_tests + self.failed_tests, self.passed_tests, self.failed_tests))
