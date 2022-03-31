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
"""Interpret lump data designed for Doom and Doom II.

Lumps are stored in several different binary formats. Some have header
data and others do not. The classes defined here are designed to
transform the data into named attributes, leaving the binary data
behind.

Map format: takes data from several lumps to form a complete set of
level data. Can interpret and return the data in useful ways e.g. line
and sector data for drawing a representation of the map geometry. NOT
implemented.

[patch](https://doomwiki.org/wiki/Picture_format)
"""

def read_int(data):
    """Translate an signed byte sequence to number."""
    return int.from_bytes(data, byteorder='little', signed=True)

def read_str(data):
    """Tranlate an ascii-encoded byte sequence to string.

    Some Doom strings are padded with null bytes, which are ignored.
    """
    return data.decode('ascii').strip("\0")

def read_uint(data):
    """Translate an unsigned byte sequence to number."""
    return int.from_bytes(data, byteorder='little', signed=False)

def read_uint_array(data, size):
    array = []
    for x in range(0, len(data), size):
        value = int.from_bytes(data[x: x + size], byteorder='little',
                signed=False)
        array.append(value)
    return array

class Playpal():
    """A collection of 256-color palettes."""

    def __init__(self, data):
        # TODO: ability to self-generate a palette on command instead
        map0 = []
        for x in range(0, 768, 3):
            map0.append(data[x: x + 3].hex())
        self.maps = [map0,]

    def get_translate(self, word):
        """Change greens to a classic GIBR multiplayer variant."""
        trans = 0
        if word == 'indigo':
            trans = -16
        elif word == 'brown':
            trans = -48
        elif word == 'red':
            trans = -80
        transmap = self.maps[0]
        for x in range(112, 127):
            transmap[x] = transmap[x + trans]
        return transmap


class Level():
    """Standard Doom level data.

    Doom levels consist of a uniquely-named 'Header' followed by ten
    essential lumps in the following order.

    THINGS
    LINEDEFS
    SIDEDEFS
    VERTEXES
    SEGS
    SSECTORS
    NODES
    SECTORS
    REJECT
    BLOCKMAP
    """

    def __init__(self, **lumps):
        if 'Header' in lumps:
            self.header = lumps['Header']
        if 'THINGS' in lumps:
            data = lumps['THINGS']
            self.things = []
            for x in range(0, len(data), 10):
                thing = Thing(data[x: x + 10])
                self.things.append(thing)
        if 'LINEDEFS' in lumps:
            data = lumps['LINEDEFS']
            self.linedefs = []
            for x in range(0, len(data), 14):
                linedef = Linedef(data[x: x + 14])
                self.linedefs.append(linedef)
        if 'SIDEDEFS' in lumps:
            data = lumps['SIDEDEFS']
            self.sidedefs = []
            for x in range(0, len(data), 30):
                sidedef = Sidedef(data[x: x + 30])
                self.sidedefs.append(sidedef)
        if 'VERTEXES' in lumps:
            vertex_data = lumps['VERTEXES']
            self.vertexes = []
            for x in range(0, len(vertex_data), 4):
                vertex = Vertex(vertex_data[x: x + 4])
                self.vertexes.append(vertex)


class Vertex():
    def __init__(self, data):
        self.x = read_int(data[0: 2])
        self.y = read_int(data[2: 4])


class Thing():
    def __init__(self, data):
        self.x = read_int(data[0: 2])
        self.y = read_int(data[2: 4])
        self.angle = read_int(data[4: 6])
        self.type = read_int(data[6: 8])
        self.flags = read_int(data[8: 10])


class Linedef():
    def __init__(self, data):
        self.start = read_uint(data[0: 2])
        self.end = read_uint(data[2: 4])
        self.flags = read_uint(data[4: 6])
        self.type = read_uint(data[6: 8])
        self.tag = read_uint(data[8: 10])
        self.front = read_uint(data[10: 12])
        self.back = read_uint(data[12: 14])


class Sidedef():
    def __init__(self, data):
        self.xoffs = read_int(bytemap[0: 2])
        self.yoffs = read_int(bytemap[2: 4])
        self.upper = read_str(bytemap[4: 12])
        self.lower = read_str(bytemap[12: 20])
        self.middle = read_str(bytemap[20: 28])
        self.sector = read_int(bytemap[28: 30])


if __name__ == "__main__":
    print(__doc__)
