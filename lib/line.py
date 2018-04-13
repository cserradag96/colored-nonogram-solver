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

from term import Term
from clause import Clause

#######################################################################################################################
# CLASS DECLARATION:
#######################################################################################################################

class Line:
    index = 0

    def __init__(self, length, groups=[]):
        self.length = length
        self.groups = groups
        self.index = self.__class__.index

        self.__class__.index += 1

    def startLimit(self, group):
        return self.length - len(group)

    def addClauses(self, expression):
        self.groupsStart(expression)           # Los grupos deben comenzar en alguna parte
        self.groupDosentDuplicate(expression)  # Los grupos solo deben empezar una vez
        self.groupToCell(expression)           # El grupo implica que las celdas que contienen estan coloreadas
        self.cellToGroup(expression)           # Una celda esta coloreada solo si esta en un grupo
        self.groupOrder(expression)            # Mantener orden de los grupos

    def groupsStart(self, expression):
        for index, group in enumerate(self.groups):
            terms = []
            for start in range(self.startLimit(group) + 1):
                terms.append(Term(self.groupStartName(index, start)))
            expression.add(Clause(terms))

    def groupDosentDuplicate(self, expression):
        for index, group in enumerate(self.groups):
            for pos in range(self.startLimit(group) + 1):
                for nextPos in range(pos + 1, self.startLimit(group) + 1):
                    terms = []
                    terms.append(-Term(self.groupStartName(index, pos)))
                    terms.append(-Term(self.groupStartName(index, nextPos)))
                    expression.add(Clause(terms))

    def groupToCell(self, expression):
        for index, group in enumerate(self.groups):
            for start in range(self.startLimit(group) + 1):
                for i in range(len(group)):
                    terms = []
                    terms.append(-Term(self.groupStartName(index, start)))
                    terms.append(Term(self.cellName(start + i)))
                    expression.add(Clause(terms))

    def cellToGroup(self, expression):
        for cell in range(self.length):
            terms = []
            terms.append(-Term(self.cellName(cell)))

            for index, group in enumerate(self.groups):
                for position in range(min(self.startLimit(group), cell) + 1):
                    if (position + len(group) > cell):
                        terms.append(Term(self.groupStartName(index, position)))

            expression.add(Clause(terms))

    def groupOrder(self, expression):
        if (len(self.groups) < 2): return

        for i in range(len(self.groups) - 1):
            for first in range(self.startLimit(self.groups[i]) + 1):
                for second in range(self.startLimit(self.groups[i + 1]) + 1):
                    eqColor = self.groups[i].color.name == self.groups[i + 1].color.name
                    length0 = second < first + len(self.groups[i]) + 1
                    length1 = second < first + len(self.groups[i])

                    if (eqColor and length0) or (not eqColor and length1):
                        terms = []
                        terms.append(-Term(self.groupStartName(i, first)))
                        terms.append(-Term(self.groupStartName(i + 1, second)))
                        expression.add(Clause(terms))

#######################################################################################################################
# :)
#######################################################################################################################
