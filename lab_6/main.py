import math
import os

from input.parser import Parser
import numpy as np
import random as rand


def sigmoid(input_z):
    return 1 / (1 + pow(math.e, -input_z))


def sigmoid_derivative(input_z):
    sigmoid_result = sigmoid(input_z)
    return sigmoid_result * (1 - sigmoid_result)


def get_error(results, outputs):
    return np.divide(np.sum(np.power(np.subtract(results, outputs), 2), 2))


def forward_prop(weights, biases, instances):
    print(instances.dtype)
    z0 = np.add(weights[0].dot(instances.transpose()), biases[0].reshape(12, 1))
    y0 = sigmoid(z0)
    z1 = np.add(np.dot(weights[1], y0), biases[1].reshape(3, 1))
    y1 = sigmoid(z1)
    return z0, y0, z1, y1


def forward_prop_instance(weights, biases, instance):
    z0 = np.add(weights[0].dot(instance), biases[0])
    y0 = sigmoid(z0)
    z1 = np.add(np.dot(weights[1], y0), biases[1])
    y1 = sigmoid(z1)
    return y1


# TO DO: transform a name into an (3, 1) vector
# have 2 0's and 1 for the class it belongs to
# example: IRIS_VERSICOLOR = [0, 1, 0]
def encode_results(dataset):
    pass


def get_weights_and_biases(hidden_size, input_size=4, output_size=3):
    weights = np.array([np.array([[rand.uniform(-0.1, 0.1) for _ in range(input_size)] for _ in range(hidden_size)]),
                       np.array([[rand.uniform(-0.1, 0.1) for _ in range(hidden_size)] for _ in range(output_size)])], dtype=object)
    biases = np.array([np.array([rand.uniform(-0.1, 0.1) for _ in range(hidden_size)]),
                      np.array([rand.uniform(-0.1, 0.1) for _ in range(output_size)])], dtype=object)

    return weights, biases


def train(nr_epochs=25, learning_rate=0.6):
    pass

def separate_data(train_data):
    train_data_no_res = []
    out_data = []
    for line in train_data:
        line_arr = line[:-1]
        out_arr = line[-1]
        train_data_no_res.append(line_arr)
        out_data.append(out_arr)
    return np.array(train_data_no_res), np.array(out_data)


def main():
    data_file = os.path.join("input", "iris.data")
    test_parser = Parser(data_file)
    train_data, test_data = test_parser.parse()

    # print(train_data)
    # print(test_data)
    hidden_size = 12
    weights, biases = get_weights_and_biases(hidden_size)
    # print(weights)
    # print(biases)

    input_train, target_train = separate_data(train_data)
    print(forward_prop(weights, biases, input_train))


if __name__ == '__main__':
    main()
