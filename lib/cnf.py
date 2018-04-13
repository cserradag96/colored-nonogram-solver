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
# CLASS DECLARATION:
#######################################################################################################################

class CNF:
    def __init__(self):
        self.clauses = []
        self.variables = []
        self.map = {}

    def add(self, clause):
        for term in clause.terms:
            name = term.name
            if not (name in self.map):
                self.map[name] = len(self.variables)
                self.variables.append(name)
        self.clauses.append(clause)

    def __str__(self):
        header = "p cnf " + str(len(self.variables)) + " " + str(len(self.clauses)) + "\n"
        cnf = ""
        for clause in self.clauses:
            for term in clause.terms:
                cnf += ("-" if term.negative else "") + str(self.map[term.name] + 1) + " "
            cnf += "0\n"
        return header + cnf

    def parse(self, file_path):
        variables = []
        with open(file_path) as file:
            for index, line in enumerate(file):
                if index == 1:
                    variables = [x > 0 for x in list(map(int, line.split(' ')))[:-1]]
        return variables

    def solve(self, file_path):
        values = self.parse(file_path)
        solution = {}
        for i in range(len(values)):
            solution[self.variables[i]] = values[i]

        return solution

#######################################################################################################################
# :)
#######################################################################################################################
