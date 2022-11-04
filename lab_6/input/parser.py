from collections import defaultdict


class Parser:
    def __init__(self, filename) -> None:
        self.filename = filename

    def parse(self) -> tuple[list, list]:
        data = defaultdict(lambda: list())
        with open(self.filename) as fd:
            lines = fd.readlines()
        for line in lines:
            line = line[:-1]
            attr_values = line.split(",")
            out_value = attr_values[-1]
            data[out_value].append(attr_values)

        train_data = []
        test_data = []
        # 80% training; 20% test
        for item in data.items():
            total_size = len(item[1])
            train_size = int(total_size * 0.8)
            train_data += item[1][:train_size]
            test_data += item[1][train_size:]

        return train_data, test_data
