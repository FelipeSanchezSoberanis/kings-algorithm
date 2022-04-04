import scipy.stats as sp_stats
from string import ascii_uppercase
from prettytable import PrettyTable, ALL
import numpy as np
import json


class Table:
    def __init__(self, file_path):
        with open(file_path) as file:
            self.matrix = np.array(json.load(file))
        self.no_rows = len(self.matrix)
        self.no_cols = len(self.matrix[0])

        self.wjs = []
        self.wis = []

        self.wj_ranks = []

        self.calculate_wjs()
        self.calculate_wis()

        self.calculate_wj_ranks()
        self.calculate_wi_ranks()

    def sort_rows(self):

        pass

    def calculate_wj_ranks(self):
        ordinal_list = sp_stats.rankdata(self.wjs, method="ordinal")
        self.wj_ranks = [int(number) for number in ordinal_list]
        self.wj_ranks.reverse()

    def calculate_wi_ranks(self):
        ordinal_list = sp_stats.rankdata(self.wis, method="ordinal")
        self.wi_ranks = [int(number) for number in ordinal_list]
        self.wi_ranks.reverse()

    def calculate_wjs(self):
        for i in range(self.no_rows):
            wj = 0
            for j in range(self.no_cols):
                wj += self.matrix[i][j] * 2 ** (self.no_cols - j - 1)
            self.wjs.append(wj)

    def calculate_wis(self):
        for j in range(self.no_cols):
            wi = 0
            for i in range(self.no_rows):
                wi += self.matrix[i][j] * 2 ** (self.no_rows - i - 1)
            self.wis.append(wi)

    def to_table(self, print=["wi", "wj"]):
        table_data = []

        for row in self.matrix:
            new_row = []
            for col in row:
                if col == 1:
                    new_row.append(col)
                else:
                    new_row.append("")
            table_data.append(new_row)

        table = PrettyTable()
        table.hrules = ALL

        field_names = []
        for i in range(self.no_cols):
            field_names.append(ascii_uppercase[i])

        col_names = []
        for i in range(self.no_rows):
            col_names.append("M{}".format(i + 1))

        table.field_names = [""] + field_names + ["wj"] + ["rank"]

        for (i, row) in enumerate(table_data):
            table.add_row([col_names[i]] + row + [self.wjs[i]] + [self.wj_ranks[i]])
        table.add_row(["wi"] + [str(wi) for wi in self.wis] + [""] + [""])
        table.add_row(["rank"] + [str(wi) for wi in self.wi_ranks] + [""] + [""])

        return table


def main():

    table = Table("data/table.json")

    print(table.to_table())
    table.sort_rows()
    print(table.to_table())

    #  matrix = np.array([[1, 2, 3], [2, 3, 1], [3, 1, 2]])
    #  print("Original matrix \n", matrix)
    #  matrix.sort(axis=0)
    #  print("Matrix sorted in axis 0 \n", matrix)


if __name__ == "__main__":
    main()
