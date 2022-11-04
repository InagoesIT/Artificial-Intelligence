import math
import os

from input.parser import Parser
import numpy as np
import random as rand


def sigmoid_function(input_z):
    return 1 / (1 + pow(math.e, -input_z))


def sigmoid_derivative(input_z):
    sigmoid_result = sigmoid_function(input_z)
    return sigmoid_result * (1 - sigmoid_result)


def get_error(results, outputs):
    # add sum after subtraction
    return np.divide(np.power(np.subtract(results, outputs), 2), 2)


# TO DO: transform a name into an (3, 1) vector
# have 2 0's and 1 for the class it belongs to
# example: IRIS_VERSICOLOR = [0, 1, 0]
def encode_results(dataset):
    pass


def get_weights_and_biases(hidden_size, input_size=4, output_size=3):
    weights = np.array([[[rand.uniform(-0.1, 0.1) for _ in range(input_size)] for _ in range(hidden_size)],
                        [[rand.uniform(-0.1, 0.1) for _ in range(hidden_size)] for _ in range(output_size)]], dtype=object)
    biases = np.array([[rand.uniform(-0.1, 0.1) for _ in range(hidden_size)],
                       [rand.uniform(-0.1, 0.1) for _ in range(output_size)]], dtype=object)

    return weights, biases


def train(nr_epochs=25, learning_rate=0.6):
    pass


def main():
    data_file = os.path.join("input", "iris.data")
    test_parser = Parser(data_file)
    train_data, test_data = test_parser.parse()

    print(train_data)
    print(test_data)
    hidden_size = 12
    weights, biases = get_weights_and_biases(hidden_size)
    print(weights)
    print(biases)


if __name__ == '__main__':
    main()
