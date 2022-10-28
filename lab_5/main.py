import json
import sys
from tabulate import tabulate


class Model:
    def __init__(self, players, column_names, row_names, values):
        self.players = players
        self.column_names = column_names
        self.row_names = row_names
        self.values = values

    def pretty_print(self):
        table = [[f"{self.players[0]} / {self.players[1]}", self.column_names[0], self.column_names[1]],
                 [self.row_names[0], self.values[0][0], self.values[0][1]],
                 [self.row_names[1], self.values[1][0], self.values[1][1]]]
        print(tabulate(table))


class Parser:
    def __init__(self, filename: str):
        self.filename = filename

    @staticmethod
    def get_line_no_empty_spaces(elements):
        return list(filter(lambda x: x != '', elements))

    def parse_line(self, line, players):
        line = self.get_line_no_empty_spaces(line.strip().split(' '))
        players.append(line[0])
        return line[1:]

    def parse_data_into_model(self):
        players = []
        rows = []
        columns = []
        values = []

        with open(self.filename) as fd:
            lines = fd.readlines()
            row_names = self.parse_line(lines[0], players)
            column_names = self.parse_line(lines[1], players)

            for line_index, line in enumerate(lines[2:]):
                row = []
                tuples_data = self.get_line_no_empty_spaces(line.split(' '))
                for column_index, tuple_data in enumerate(tuples_data):
                    players_values = tuple(int(el) for el in tuple_data.split('/'))
                    row.append(players_values)
                values.append(row)

        return Model(players, column_names, row_names, values)


if __name__ == '__main__':
    parser = Parser("data.txt")
    model = parser.parse_data_into_model()
    model.pretty_print()
