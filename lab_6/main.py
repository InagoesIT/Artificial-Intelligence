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
    print(type(weights[0]))
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
    return z0, y0, z1, y1


def get_one_hot_target(target):
    IRIS_SETOSA = "Iris-setosa"
    IRIS_VERSICOLOR = "Iris-versicolor"
    IRIS_VIRGINICA = "Iris-virginica"
    IRIS_SETOSA_ARR = [1, 0, 0]
    IRIS_VERSICOLOR_ARR = [0, 1, 0]
    IRIS_VIRGINICA_ARR = [0, 0, 1]

    if target == IRIS_SETOSA:
        return IRIS_SETOSA_ARR
    elif target == IRIS_VERSICOLOR:
        return IRIS_VERSICOLOR_ARR
    elif target == IRIS_VIRGINICA:
        return IRIS_VIRGINICA_ARR
    return None


def get_one_hot_batch(batch_targets):
    transformed = []

    for item in batch_targets:
        transformed.append(get_one_hot_target(item))

    return np.array(transformed)


def get_weights_and_biases(hidden_size, input_size=4, output_size=3):
    weights = np.array([np.array([[rand.uniform(-0.1, 0.1) for _ in range(input_size)] for _ in range(hidden_size)]),
                        np.array([[rand.uniform(-0.1, 0.1) for _ in range(hidden_size)] for _ in range(output_size)])],
                       dtype=object)
    biases = np.array([np.array([rand.uniform(-0.1, 0.1) for _ in range(hidden_size)]),
                       np.array([rand.uniform(-0.1, 0.1) for _ in range(output_size)])], dtype=object)

    return weights, biases


def get_batches(train_data, train_target, batch_size):
    training_size = len(train_data)
    batches_data = []
    batches_target = []
    for batch_start, batch_end in zip(range(0, training_size, batch_size),
                                      range(batch_size, training_size, batch_size)):
        batches_data.append(np.array(train_data[batch_start:batch_end][:]))
        batches_target.append(np.array(get_one_hot_batch(train_target[batch_start:batch_end])))

    return batches_data, batches_target


def train(train_data, train_target, weights, biases, nr_epochs=25, learning_rate=0.6, batch_size=20):
    batches_data, batches_target = get_batches(train_data, train_target, batch_size)

    for epoch_nr in range(nr_epochs):
        for batch_index in range(len(batches_target)):
            z0, y0, z1, y1 = forward_prop(weights, biases, batches_data[batch_index])
            # TODO George will make these 2 work
            dw1, dw2, db1, db2 = backward_prop(z0, batches_data[batch_index], y0, y1, weights_level_2=weights[1],
                                               targets=batches_target[batch_index])
            weights, biases = update_params(weights, biases, dw1, dw2, db1, db2, learning_rate)
        print(f"epoch = {epoch_nr}")
        if epoch_nr % 5 == 0:
            print(f"the accuracy for the training set is: {get_accuracy(weights, biases, training_set)}")
            print(f"the accuracy for the validation set is: {get_accuracy(weights, biases, validation_set)}")
    return weights, biases


def main():
    data_file = os.path.join("input", "iris.data")
    test_parser = Parser(data_file)
    train_data, train_target, test_data, train_target = test_parser.parse()

    hidden_size = 24
    weights, biases = get_weights_and_biases(hidden_size)
    batches_data, batches_target = get_batches(train_data, train_target, 20)
    z0, y0, z1, y1 = forward_prop(weights, biases, batches_data[0])


if __name__ == '__main__':
    main()
