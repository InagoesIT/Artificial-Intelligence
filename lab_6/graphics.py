from collections import defaultdict

import numpy
import numpy as np
from matplotlib import pyplot as plt, cm


class Graphics:
    def __init__(self, data=None, expected_results=None, results=None, must_process=False):
        processed_data = []
        curr_index = defaultdict(lambda: 0)
        if must_process:
            no_params = len(data[0])
            processed_data = [np.zeros(len(data)) for _ in data[0]]
            for instance in data:
                for index, element in enumerate(instance):
                    pos = curr_index[index]
                    processed_data[index][pos] = element
                    curr_index[index] += 1

            self.data = processed_data
        else:
            self.data = data
        self.expected_results = expected_results
        self.results = results
        self.no_dimensions = len(data)
        self.dirname = "default"

    def save_visual_with_axis(self, x_index, y_index, z_index):
        x = np.array(self.data[x_index])
        y = np.array(self.data[y_index])
        z = np.array(self.data[z_index])
        colo = [x]

        fig = plt.figure(figsize=(10, 10))
        ax = fig.add_subplot(111, projection='3d')

        # setting color bar
        color_map = cm.ScalarMappable(cmap=cm.Greens_r)
        color_map.set_array(colo)

        # creating the heatmap
        img = ax.scatter(x, y, z, marker='s',
                         s=200, color='green')
        plt.colorbar(color_map)

        # adding title and labels
        ax.set_title("3D Heatmap")
        ax.set_xlabel('X-axis')
        ax.set_ylabel('Y-axis')
        ax.set_zlabel('Z-axis')

        # displaying plot
        plt.show()

    def save_visual_representation(self, dirname="default"):
        self.dirname = dirname
        for x in range(0, self.no_dimensions - 2):
            for y in range(x + 1, self.no_dimensions - 1):
                for z in range(y + 1, self.no_dimensions):
                    self.save_visual_with_axis(x, y, z)

def filter_data(data_arr, expected_result, result, must_process=False):
    filtered_data = []
    if must_process:
        for index in range(len(data_arr[0])):
            if expected_result[index] != result[index]:
                reversed_data = np.zeros(len(data_arr))
                for value_index, value in enumerate(data_arr):
                    reversed_data[value_index] = value[index]
                filtered_data.append(reversed_data)
    else:
        for index, data in enumerate(data_arr):
            if expected_result[index] != result[index]:
                filtered_data.append(data)
    return filtered_data


if __name__ == "__main__":
    data_arr = [numpy.array([1, 2, 3]),
                numpy.array([1, 2, 3]),
                numpy.array([1, 2, 3])]
    data_arr = filter_data(must_process=True, data_arr=data_arr, result=[True, True, True], expected_result=[False, False, False])
    graphics = Graphics(data=data_arr, must_process=True)
    graphics.save_visual_representation()
