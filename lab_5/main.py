import json
import sys


class Model:
    def __init__(self, players, columns, rows, values):
        self.players = players
        self.columns = columns
        self.rows = rows
        self.values = values

    def not_that_pretty_print(self):
        json.dump(self.values, sys.stdout, indent=4)

class Parser:
    def __init__(self, filename: str):
        self.filename = filename

    def get_lines_no_empty_spaces(self, elements):
        return list(filter(lambda x: x != '', elements))

    def parse_line(self, line, players, to_be_filled):
        line = self.get_lines_no_empty_spaces(line.strip().split(' '))
        players.append(line[0])
        to_be_filled = line[1:]
        return to_be_filled

    def make_space_for(self, values, player, line_index):
        if line_index not in values[player]:
            values[player][line_index] = dict()

    def parse_data_into_model(self):
        players = []
        rows = []
        columns = []

        values = dict()
        values[0] = dict()
        values[1] = dict()
        with open(self.filename) as fd:
            lines = fd.readlines()

            self.parse_line(lines[0], players, rows)
            self.parse_line(lines[1], players, columns)
            for line_index, line in enumerate(lines[2:], start=0):
                tuples_data = self.get_lines_no_empty_spaces(line.split(' '))
                for column_index, tuple_data in enumerate(tuples_data):
                    player_1, player_2 = [int(el) for el in tuple_data.split('/')]
                    self.make_space_for(values, 0, line_index)
                    self.make_space_for(values, 1, line_index)

                    values[0][line_index][column_index] = player_1
                    values[1][line_index][column_index] = player_2
        return Model(players, columns, rows, values)


if __name__ == '__main__':
    parser = Parser("data.txt")
    model = parser.parse_data_into_model()
    model.not_that_pretty_print()
