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
        linedef['start'] = read_uint(bytemap[i: i + 2])
        linedef['end'] = read_uint(bytemap[i + 2: i + 4])
        linedef['flags'] = read_uint(bytemap[i + 4: i + 6])
        linedef['type'] = read_uint(bytemap[i + 6: i + 8])
        linedef['tag'] = read_uint(bytemap[i + 8: i + 10])
        linedef['front'] = read_uint(bytemap[i + 10: i + 12])
        linedef['back'] = read_uint(bytemap[i + 12: i + 14])
        linedefs.append(linedef)
    return linedefs

def load_patch(filename, maxw=256):
    """Return each part of the file header in a dictionary."""
    with open(filename, 'rb') as file:
        width = read_uint(file.read(2))
        height = read_uint(file.read(2))
        leftoffset = read_int(file.read(2))
        topoffset = read_int(file.read(2))
        columnofs = []
        for i in range(width % maxw):
            columnofs.append(read_int(file.read(4))
    header = dict(width=width,height=height,leftoffset=leftoffset,
                  topoffset=topoffset,columnofs=columnofs)
    if width > maxw:
        # TODO: provide a way to limit max width and max columns in
        # case of invalid or corrupted file, and provide explicit
        # overrides as parameters, and fail gracefully
        print("patter: WARNING width >", maxw, "likely not a patch lump")
        print("patter: aborting")
        return False
    else:
        print("width:", width)
        print("height:", height)
        print("leftoffset:", leftoffset)
        print("topoffset:", topoffset)
        print("columnofs:", columnofs)
    with open(filename, 'rb') as file:
        columns = []  # array to hold picture columns
        for i, offset in enumerate(columnofs):
            file.seek(offset)
            topdelta = 0
            posts = []  # array to hold posts in column
            while topdelta < 255:  # read posts until terminator
                topdelta = read_uint(file.read(1))
                length = read_uint(file.read(1))
                unused1 = read_uint(file.read(1))
                data = file.read(length)
                unused2 = read_uint(file.read(1))
                if topdelta < 255:
                    posts.append(dict(topdelta=topdelta,data=data))
            columns.append(posts)
    return header, columns

def read_sidedefs(bytemap):
    sidedefs = []
    for i in range(0, len(bytemap), 30):
        sidedef = {}
        sidedef['xoffs'] = read_int(bytemap[i: i + 2])
        sidedef['yoffs'] = read_int(bytemap[i + 2: i + 4])
        sidedef['upper'] = read_str(bytemap[i + 4: i + 12])
        sidedef['lower'] = read_str(bytemap[i + 12: i + 20])
        sidedef['middle'] = read_str(bytemap[i + 20: i + 28])
        sidedef['sector'] = read_int(bytemap[i + 28: i + 30])
        sidedefs.append(sidedef)
    return sidedefs

def load_vertexes(bytemap):
    """Return all x,y coordiante pairs from a 'VERTEXES' lump.

    'VERTEXES' is the fourth lump after the map 'Header' lump in a
    WAD."""
    vertexes = []
    for i in range(0, len(bytemap), 4):
        vertex = {}
        vertex['x'] = read_int(bytemap[i: i + 2])
        vertex['y'] = read_int(bytemap[i + 2: i + 4])
        vertexes.append(vertex)
    return vertexes

def read_int16_t(data):
    return int.from_bytes(data[:2], byteorder='little', signed=True)

def read_uint16_t(data):
    return int.from_bytes(data[:2], byteorder='little', signed=False)

def read_int(data):
    return int.from_bytes(data, byteorder='little', signed=True)

def read_str(data):
    return data.decode('ascii').strip("\0")

def read_uint(data):
    return int.from_bytes(data, byteorder='little', signed=False)

if __name__ == "__main__":
    print(__doc__)
