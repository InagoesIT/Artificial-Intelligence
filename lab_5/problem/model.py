from tabulate import tabulate


class Model:
    def __init__(self, players, column_names, row_names, values):
        self.players = players
        self.column_names = column_names
        self.row_names = row_names
        self.values = values
        self.n = len(row_names)
        self.m = len(column_names)

    def pretty_print(self):
        table = [[f"{self.players[0]} / {self.players[1]}", self.column_names[0], self.column_names[1]],
                 [self.row_names[0], self.values[0][0], self.values[0][1]],
                 [self.row_names[1], self.values[1][0], self.values[1][1]]]
        print(tabulate(table))
