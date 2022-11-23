from collections import defaultdict
import numpy as np


class Parser:
    def __init__(self, filename) -> None:
        self.filename = filename

    def parse(self) -> tuple[list, list, list, list]:
        data = defaultdict(lambda: list())
        with open(self.filename) as fd:
            lines = fd.readlines()
        for line in lines:
            line = line[:-1]
            attr_values = line.split(",")
            out_value = attr_values[-1]
            data[out_value].append(attr_values[:-1])

        # TODO -> FIND A BETTER FIX FOR THIS ISSUE
        data.pop('')

        train_percentage = 0.8
        train_data = []
        train_target = []
        test_data = []
        test_target = []

        # 80% training; 20% test
        for item in data.items():
            total_size = len(item[1])
            train_size = int(total_size * train_percentage)
            test_size = total_size - train_size
            train_data += item[1][:train_size]
            train_target += ([item[0]] * train_size)
            test_data += item[1][train_size:]
            test_target += ([item[0]] * test_size)

        return train_data, train_target, test_data, test_target

