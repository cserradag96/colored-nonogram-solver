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

import svgwrite
from svgwrite import cm, mm
from group import Group
from color import Color
from row import Row
from column import Column
from subprocess import Popen, PIPE, STDOUT
from os.path import basename

#######################################################################################################################
# FUNCTIONS:
#######################################################################################################################

# Read a file.non
def readNon(file_path):
    rows, columns = [], []
    with open(file_path) as file:
        c, w, h = list(map(int, file.readline().split(" ")))

        colorsMap = {}
        for i in range(c):
            color = Color(*file.readline().split(" "))
            colorsMap[color.name] = color

        for i in range(h):
            groups = []
            for group in file.readline().split(","):
                group = group.split(":")
                groups.append(Group(int(group[0]), colorsMap[group[1].strip()]))
            rows.append(Row(w, groups))

        for i in range(w):
            groups = []
            for group in file.readline().split(","):
                group = group.split(":")
                groups.append(Group(int(group[0]), colorsMap[group[1].strip()]))
            columns.append(Column(h, groups))

    return rows, columns

# Write content into file
def writeFile(content, file_path):
    with open(file_path, 'w') as file:
        file.write(str(content))

# Get id for nonogram grid variable
def varId(i, j):
    return "r" + str(i) + "c" + str(j)

# Iterator for stdout
def iterStdout(p):
    while True:
        line = p.stdout.readline()
        if not line:
            break

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
def nameSVG(file_path):
    return basename(file_path).replace(".cnon", ".svg")

# Draw background
def drawBg(dwg, width, height):
    bg = dwg.add(dwg.g(id='bg', fill='white'))
    bg.add(dwg.rect(insert=(0, 0), size=(width * cm, height * cm), fill='white'))

# Draw a cell
def drawCell(dwg, i, j, color):
    square = dwg.add(dwg.g())
    square.add(dwg.rect(insert=(j * cm, i * cm), size=(1 * cm, 1 * cm), fill=color))

# Draw grid lines
def drawGrid(dwg, width, height):
    # Draw horizontal lines
    hl = dwg.add(dwg.g(id='hl', stroke='black'))
    for i in range(height + 1):
        hl.add(dwg.line(start=(0, i * cm), end=(width * cm, i * cm)))

    # Draw vertical lines
    vl = dwg.add(dwg.g(id='vl', stroke='black'))
    for i in range(width + 1):
        vl.add(dwg.line(start=(i * cm, 0), end=(i * cm, height * cm)))

# Create svg
def writeSVG(width, height, puzzle, output):
    # Create file and draw background
    dwg = svgwrite.Drawing(filename=output)
    drawBg(dwg, width, height)

    # Draw solution
    for i in range(height):
        for j in range(width):
            if puzzle[i][j]:
                drawCell(dwg, i, j, puzzle[i][j])

    # Draw grid lines and store
    drawGrid(dwg, width, height)
    dwg.save()

#######################################################################################################################
# :)
#######################################################################################################################
