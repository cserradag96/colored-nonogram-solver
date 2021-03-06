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

class Group:
    def __init__(self, length, color):
        self.length = length
        self.color = color

    def __len__(self):
        return self.length

    def __str__(self):
        return str(self.length) + ":" + str(self.color)

#######################################################################################################################
# :)
#######################################################################################################################
