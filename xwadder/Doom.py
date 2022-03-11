#!/usr/bin/env python3
#Copyright 2022 Eric Duhamel
#
#    This file is part of Wadder.
#
#    Wadder is free software: you can redistribute it and/or modify it
#    under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    Wadder is distributed in the hope that it will be useful, but
#    WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
#    General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with Wadder. If not, see <https://www.gnu.org/licenses/>.
#
"""
Functions for loading data from lumps in formats originally designed
for Doom and Doom II.
"""

def read_things(bytemap):
    """Return all x,y coordiante pairs from a 'THINGS' lump.

    'THINGS' is the fourth lump after the map 'Header' lump in a
    WAD."""
    things = []
    for i in range(0, len(bytemap), 2):
        thing = {}
        thing['x'] = read_int16_t(bytemap[i:])
        thing['y'] = read_int16_t(bytemap[i + 2:])
        thing['angle'] = read_int16_t(bytemap[i + 4:])
        thing['type'] = read_int16_t(bytemap[i + 6:])
        thing['flags'] = read_int16_t(bytemap[i + 8:])
        things.append(thing)
    return things

def load_linedefs(bytemap):
    linedefs = []
    for i in range(0, len(bytemap), 14):
        linedef = {}
        linedef['start'] = readuint(bytemap[i: i + 2])
        linedef['end'] = readuint(bytemap[i + 2: i + 4])
        linedef['flags'] = readuint(bytemap[i + 4: i + 6])
        linedef['type'] = readuint(bytemap[i + 6: i + 8])
        linedef['tag'] = readuint(bytemap[i + 8: i + 10])
        linedef['front'] = readuint(bytemap[i + 10: i + 12])
        linedef['back'] = readuint(bytemap[i + 12: i + 14])
        linedefs.append(linedef)
    return linedefs

def read_sidedefs(bytemap):
    sidedefs = []
    for i in range(0, len(bytemap), 30):
        sidedef = {}
        sidedef['xoffs'] = readint(bytemap[i: i + 2])
        sidedef['yoffs'] = readint(bytemap[i + 2: i + 4])
        sidedef['upper'] = readstr(bytemap[i + 4: i + 12])
        sidedef['lower'] = readstr(bytemap[i + 12: i + 20])
        sidedef['middle'] = readstr(bytemap[i + 20: i + 28])
        sidedef['sector'] = readint(bytemap[i + 28: i + 30])
        sidedefs.append(sidedef)
    return sidedefs

def load_vertexes(bytemap):
    """Return all x,y coordiante pairs from a 'VERTEXES' lump.

    'VERTEXES' is the fourth lump after the map 'Header' lump in a
    WAD."""
    vertexes = []
    for i in range(0, len(bytemap), 4):
        vertex = {}
        vertex['x'] = readint(bytemap[i: i + 2])
        vertex['y'] = readint(bytemap[i + 2: i + 4])
        vertexes.append(vertex)
    return vertexes

def readint(data):
    return int.from_bytes(data, byteorder='little', signed=True)

def read_int16_t(data):
    return int.from_bytes(data[:2], byteorder='little', signed=True)

def readstr(data):
    return data.decode('ascii').strip("\0")

def readuint(data):
    return int.from_bytes(data, byteorder='little', signed=False)

if __name__ == "__main__":
    print(__doc__)
