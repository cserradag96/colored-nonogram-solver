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
    readR, readC = False, False
    rows, columns = [], []
    with open(file_path) as file:
        for line in file:
            if readC and len(columns) < width: columns.append(Column(height, [int(x) for x in line.split(",")]))
            elif readR and len(rows) < height: rows.append(Row(width, [int(x) for x in line.split(",")]))
            elif line.find("columns") >= 0: readC = True
            elif line.find("rows") >= 0: readR = True
            elif line.find("height ") >= 0: height = int(line.replace("height ", ""))
            elif line.find("width ") >= 0: width = int(line.replace("width ", ""))

    return rows, columns

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
