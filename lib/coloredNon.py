# -*- encoding: utf-8 -*-

#######################################################################################################################
# DESCRIPTION:
#######################################################################################################################

# TODO

#######################################################################################################################
# AUTHORS:
#######################################################################################################################

# Carlos Serrada, 13-11347, <cserradag96@gmail.com>
# Juan Ortiz, 13-11021 <ortiz.juan14@gmail.com>

#######################################################################################################################
# DEPENDENCIES:
#######################################################################################################################

from utils import *
from row import Row
from column import Column
from cnf import CNF

#######################################################################################################################
# CLASS DECLARATION:
#######################################################################################################################

class ColoredNon:
    def __init__(self, colors, rows, columns):
        self.colors = colors
        self.rows = rows
        self.columns = columns
        self.height = len(self.rows)
        self.width = len(self.columns)
        self.cnf = self.genCNF()

    def genCNF(self):
        expression = CNF()
        for row in self.rows: row.addClauses(expression)
        for column in self.columns: column.addClauses(expression)

        return expression

    def solve(self, output_path):
        variables = self.cnf.solve(output_path)
        if len(variables) == 0:
            print("No se pudo encontrar ninguna solución")
            sys.exit(1)

        return [[variables[varId(i, j)] for j in range(self.width)] for i in range(self.height)]

    def genBitmap(self, output_path):
        header = "P1\n" + str(self.width) + " " + str(self.height) + "\n"
        bitmap = self.paint(output_path)
        return header + bitmap + "\n"

    def paint(self, output_path):
        bitmap = [[x for x in row] for row in self.solve(output_path)]

        for i, row in enumerate(self.rows):
            start = 0
            for group in row.groups:
                painted = 0
                for k in range(start, self.width):
                    if bitmap[i][k]:
                        bitmap[i][k] = group.color
                        painted += 1
                        if painted == len(group):
                            start = k + 1
                            break

        for i in range(self.height):
            for j in range(self.width):
                if not bitmap[i][j]:
                    bitmap[i][j] = "W"

        return "\n".join([" ".join([str(x) for x in row]) for row in bitmap])

#######################################################################################################################
# :)
#######################################################################################################################
