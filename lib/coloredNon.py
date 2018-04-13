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
    def __init__(self, rows, columns):
        self.rows    = rows
        self.columns = columns
        self.height  = len(self.rows)
        self.width   = len(self.columns)
        self.cnf     = self.genCNF()

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
        bitmap = "\n".join([" ".join([boolToBits(x) for x in row]) for row in self.solve(output_path)])
        return header + bitmap + "\n"

#######################################################################################################################
# :)
#######################################################################################################################
