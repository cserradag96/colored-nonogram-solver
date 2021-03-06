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

from line import Line

#######################################################################################################################
# CLASS DECLARATION:
#######################################################################################################################

class Row(Line):
    def __init__(self, length, groups=[]):
        super(Row, self).__init__(length, groups)

    def groupStartName(self, group, start):
        return "r" + str(self.index) + "b" + str(group) + "s" + str(start)

    def cellName(self, cell):
        return "r" + str(self.index) + "c" + str(cell)

#######################################################################################################################
# :)
#######################################################################################################################
