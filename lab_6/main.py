import math
import os

import numpy

from graphics import Graphics
from input.parser import Parser
import numpy as np
import random as rand
import matplotlib.pyplot as plt
from tabulate import tabulate

IRIS_SETOSA = "Iris-setosa"
IRIS_VERSICOLOR = "Iris-versicolor"
IRIS_VIRGINICA = "Iris-virginica"
IRIS_SETOSA_INDEX = 0
IRIS_VERSICOLOR_INDEX = 1
IRIS_VIRGINICA_INDEX = 2
IRIS_SETOSA_ARR = [1, 0, 0]
IRIS_VERSICOLOR_ARR = [0, 1, 0]
IRIS_VIRGINICA_ARR = [0, 0, 1]


def sigmoid_value(input_z):
    return 1 / (1 + pow(math.e, -input_z))


def sigmoid_derivative_value(input_z):
    sigmoid_result = sigmoid(input_z)
    return sigmoid_result * (1 - sigmoid_result)


def sigmoid(values):
    return np.array([1 / (1 + pow(math.e, -_)) for _ in values])


def sigmoid_derivative(outputs):
    return np.array([sigmoid(_) * (1 - sigmoid(_)) for _ in outputs])


def get_error(results, outputs):
    return np.divide(np.sum(np.power(np.subtract(results, outputs), 2), 2))


def forward_prop(weights, biases, instances):
    # z0 = np.add((weights[0].dot(instances.transpose())), biases[0].reshape(24, 1))
    # y0 = sigmoid(z0)
    # z1 = np.add(np.dot(weights[1], y0), biases[1].reshape(3, 1))
    # y1 = sigmoid(z1)
    # return z0, y0, z1, y1
    z0 = np.add(weights[0].dot(instances.transpose()), biases[0].reshape(24, 1))
    y0 = sigmoid(z0)
    z1 = np.add(np.dot(weights[1], y0), biases[1].reshape(3, 1))
    y1 = softmax(z1)
    return z0, y0, z1, y1


def softmax(values):
    inputs_sum = sum(pow(math.e, value) for value in values)
    return np.array([pow(math.e, value) / (inputs_sum + pow(1, 0.00000001)) for value in values])


def forward_prop_instance(weights, biases, instance):
    # z0 = np.add(weights[0].dot(instance), biases[0])
    # y0 = sigmoid(z0)
    # z1 = np.add(np.dot(weights[1], y0), biases[1])
    # y1 = sigmoid(z1)
    # return z0, y0, z1, y1
    z0 = np.add(weights[0].dot(instance), biases[0])
    y0 = sigmoid(z0)
    z1 = np.add(np.dot(weights[1], y0), biases[1])
    y1 = softmax(z1)
    return z0, y0, z1, y1


def get_one_hot_target(target):
    if target == IRIS_SETOSA:
        return IRIS_SETOSA_ARR
    elif target == IRIS_VERSICOLOR:
        return IRIS_VERSICOLOR_ARR
    elif target == IRIS_VIRGINICA:
        return IRIS_VIRGINICA_ARR
    return None


def get_one_hot_batch(batch_targets):
    result = [np.array(get_one_hot_target(batch_targets[0]))]
    for i in range(1, len(batch_targets)):
        result = np.append(result, [get_one_hot_target(batch_targets[i])], axis=0)

    return result.transpose()


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
        batches_data.append(np.array(train_data[batch_start:batch_end][:], dtype=float))
        batches_target.append(np.array(get_one_hot_batch(train_target[batch_start:batch_end]), dtype=int))

    return batches_data, batches_target


def get_tuned_outputs(outputs):
    result = np.array([0 for _ in range(len(outputs))])
    result[np.argmax(outputs)] = 1
    return result


def plot_accuracies(nr_epochs, training_accuracy, test_accuracy, graph_name):
    plt.plot(nr_epochs, training_accuracy, label="training accuracy")
    plt.plot(nr_epochs, test_accuracy, label="test accuracy")
    plt.ylabel("accuracy")
    plt.xlabel("epochs")
    plt.legend()
    plt.savefig(graph_name)


def backward_prop(inputs, y0, y1, weights_level_2, targets):
    # # dC/dy * dy/dz
    # # shape = 3, 10
    # dz2 = y1 * np.subtract(1, y1) * np.subtract(y1, targets)
    # # dy/dz * (error for every neuron * weights for it)
    # # shape = 24, 10 * 24, 10(10, 4 dot 4, 24)  =>  24, 10
    # dz1 = y0 * np.subtract(1, y0) * dz2.transpose().dot(weights_level_2).transpose()
    # # (hidden -> output)
    # # 3, 10 * 10, 24 = 3, 24
    # dw2 = dz2.dot(y0.transpose())
    # db2 = np.sum(dz2, axis=1)
    # # (input -> hidden)
    # # 24, 10 * 24, 4 = 24, 4
    # dw1 = dz1.dot(inputs)
    # db1 = np.sum(dz1, axis=1)
    #
    # return dw1, dw2, db1, db2

    # dC/dy * dy/dz
    # shape = 10, 50
    dz2 = -1 / len(targets[0]) * np.subtract(targets, y1)
    # dy/dz * (error for every neuron * weights for it)
    # shape = 100, 50 * 100, 50(50, 10 dot 10, 100)  =>  100, 50
    dz1 = y0 * np.subtract(1, y0) * dz2.transpose().dot(weights_level_2).transpose()
    # (hidden -> output)
    # 10, 50 * 50, 100 = 10, 100
    dw2 = dz2.dot(y0.transpose())
    db2 = np.sum(dz2, axis=1)
    # (input -> hidden)
    # 100, 50 * 50, 784 = 100, 784
    dw1 = dz1.dot(inputs)
    db1 = np.sum(dz1, axis=1)

    return dw1, dw2, db1, db2


def update_params(weights, biases, dw1, dw2, db1, db2, learning_rate):
    weights[0] = weights[0] - learning_rate * dw1
    weights[1] = weights[1] - learning_rate * dw2
    biases[0] = biases[0] - learning_rate * db1
    biases[1] = biases[1] - learning_rate * db2

    return weights, biases


def train(train_data, train_target, test_data, test_target, weights, biases, nr_epochs=400, learning_rate=0.01,
          batch_size=10):
    batches_data, batches_target = get_batches(train_data, train_target, batch_size)
    training_accuracy = []
    test_accuracy = []

    for epoch_nr in range(nr_epochs):
        for batch_index in range(len(batches_target)):
            z0, y0, z1, y1 = forward_prop(weights, biases, batches_data[batch_index])
            dw1, dw2, db1, db2 = backward_prop(batches_data[batch_index], y0, y1, weights_level_2=weights[1],
                                               targets=batches_target[batch_index])
            weights, biases = update_params(weights, biases, dw1, dw2, db1, db2, learning_rate)

        training_accuracy.append(get_accuracy(weights, biases, train_data, train_target)[0])
        test_accuracy.append(get_accuracy(weights, biases, test_data, test_target)[0])

    plot_accuracies([i for i in range(nr_epochs)], training_accuracy, test_accuracy, "graph")
    get_confusion_matrix(weights, biases, train_data, train_target)

    return weights, biases


def get_accuracy(weights, biases, dataset_data, dataset_target):
    wrong_classified_nr = 0
    wrong_classified_data = []
    dataset_size = len(dataset_data)

    for i in range(dataset_size):
        label = dataset_target[i]
        z0, y0, z1, y1 = forward_prop_instance(weights, biases, np.array(dataset_data[i], dtype=float))
        y1 = get_tuned_outputs(y1)
        label_arr = get_one_hot_target(label)

        if not np.array_equal(y1, label_arr):
            wrong_classified_nr += 1
            wrong_classified_data += [[dataset_data[i], label_arr, list(y1)]]

    return (dataset_size - wrong_classified_nr) / dataset_size * 100, wrong_classified_data


def get_predictions(weights, biases, dataset_data):
    z0, y0, z1, y1 = forward_prop(weights, biases, dataset_data)
    # get the predicted class for every output
    return [get_tuned_outputs(y1[i]) for i in y1]


def get_confusion_matrix(weights, biases, dataset_data, dataset_target):
    wrong_count, wrong_classified_instances = get_accuracy(weights, biases, dataset_data, dataset_target)
    confusion_matrix = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]

    for instance in wrong_classified_instances:
        if instance[1] == IRIS_SETOSA_ARR:
            if instance[2] == IRIS_VERSICOLOR_ARR:
                confusion_matrix[0][1] += 1
            else:
                confusion_matrix[0][2] += 1
        elif instance[1] == IRIS_VERSICOLOR_ARR:
            if instance[2] == IRIS_SETOSA_ARR:
                confusion_matrix[1][0] += 1
            else:
                confusion_matrix[1][2] += 1
        else:
            if instance[2] == IRIS_SETOSA_ARR:
                confusion_matrix[2][0] += 1
            else:
                confusion_matrix[2][1] += 1

    confusion_matrix[0][0] = dataset_target.count(IRIS_SETOSA) - confusion_matrix[0][1] - confusion_matrix[0][2]
    confusion_matrix[1][1] = dataset_target.count(IRIS_VERSICOLOR) - confusion_matrix[1][0] - confusion_matrix[1][2]
    confusion_matrix[2][2] = dataset_target.count(IRIS_VIRGINICA) - confusion_matrix[2][0] - confusion_matrix[2][1]

    table = [["", IRIS_SETOSA, IRIS_VERSICOLOR, IRIS_VIRGINICA],
             [IRIS_SETOSA, confusion_matrix[0][0], confusion_matrix[0][1], confusion_matrix[0][2]],
             [IRIS_VERSICOLOR, confusion_matrix[1][0], confusion_matrix[1][1], confusion_matrix[1][2]],
             [IRIS_VIRGINICA, confusion_matrix[2][0], confusion_matrix[2][1], confusion_matrix[2][2]]
             ]
    print()
    print("~" * 10 + "THE CONFUSION MATRIX" + "~" * 10)
    print(tabulate(table))
    return confusion_matrix


def main():
    data_file = os.path.join("input", "iris.data")
    test_parser = Parser(data_file)
    train_data, train_target, test_data, test_target = test_parser.parse()

    hidden_size = 24
    weights, biases = get_weights_and_biases(hidden_size)
    # batches_data, batches_target = get_batches(train_data, train_target, 10)
    print(f"accuracy without any training: {get_accuracy(weights, biases, train_data, train_target)[0]}")
    get_confusion_matrix(weights, biases, train_data, train_target)
    weights, biases = train(train_data, train_target, test_data, test_target, weights, biases)

    wrong_classified = get_accuracy(weights, biases, train_data, train_target)[1]
    data_arr = [
        numpy.array([float(as_num) for as_num in element[0]])
        for element in wrong_classified]
    expected_results = [element[1] for element in wrong_classified]
    results = [element[2] for element in wrong_classified]


    print(wrong_classified)
    graphics = Graphics(data=data_arr,
                        expected_results=expected_results,
                        results=results,
                        must_process=True)
    graphics.save_visual_representation()

if __name__ == '__main__':
    main()
