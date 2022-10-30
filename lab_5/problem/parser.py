from problem.model import Model


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
