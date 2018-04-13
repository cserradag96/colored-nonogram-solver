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

from row import Row
from column import Column
from subprocess import Popen, PIPE, STDOUT
from os.path import basename

#######################################################################################################################
# FUNCTIONS:
#######################################################################################################################

# Read a file.non
def readNon(file_path):
    colors, rows, columns = {}, [], []
    with open(file_path) as file:
        c, w, h = list(map(int, file.readline().split(",")))

        for i in range(c):
            key, value = list(map(strip, file.readline().split(",")))
            colors[key] = value

        for i in range(h):
            rows.append(Row(w, [x for x in file.readline().split(",")]))

        for i in range(w):
            columns.append(Column(h, [x for x in file.readline().split(",")]))

    return colors, rows, columns

# Write content into file
def writeFile(content, file_path):
    with open(file_path, 'w') as file:
        file.write(str(content))

# Translate booleans into bits string
def boolToBits(x):
    return '1' if x else '0'

# Get id for nonogram grid variable
def varId(i, j):
    return "r" + str(i) + "c" + str(j)

# Iterator for stdout
def iterStdout(p):
    while True:
        line = p.stdout.readline()
        if not line: break
        yield str(line)[2:-3]

# Minisat pipe
def minisat(input_path, output_path):
    print("")
    command = "./minisat/core/minisat " + input_path + " " + output_path
    process = Popen(command.split(), stdout=PIPE, stderr=STDOUT)
    for line in iterStdout(process):
        print(line)

# Function to print verbose messages
def printStatus(status):
    separator = "\n======================\n"
    message = separator + "# " + status + separator
    print(message, end="")

# Extract name from file_path and add pbm format
def namePBM(file_path):
    return basename(file_path)[:-4] + ".pbm"

#######################################################################################################################
# :)
#######################################################################################################################
