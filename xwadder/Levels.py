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
a module for working with *OOM map lumps

WORK-IN-PROGRESS

Extract an individual map (consisting of several lumps) into a
directory or a WAD file.

The original DOOM map format consists of one empty (0 byte) "header"
lump followed by exactly ten lumps named THINGS, LINEDEFS, SIDEDEFS,
VERTEXES, SEGS, SSECTORS, NODES, SECTORS, REJECT, and BLOCKMAP. To
extract, simply find the header named with the ExMy or MAPxy convention
and load it plus the following ten lumps into a dictionary; or save
it plus the following ten lumps into a directory named after the
header.

Other map formats can have more or less lumps. Some formats use a
"footer" to indicate the end of the set of map lumps. Some formats may
use a text file to dilineate the beginning and end of each set of map
lumps.

This module can extract and reinsert maps when working from a valid
WAD as a source, but will require third-party tools (such as a
node-builder) to generate maps from scratch.
"""
import os
import sys

def main():
    filename = sys.argv[-1]
    if os.path.isfile(filename):
        res = 64
        width, height, origin = scale(res)
        file = open(filename, 'rb')
        for arg in sys.argv:
            if arg[0:13] == "--resolution=":
                res = int(arg[13:])
                width, height, origin = scale(res)
        bits, intmap = load_maps(filename, res)
        save_bitmap(bits, width, height, "vertexes")
        save_graymap(intmap, width, height, "vertexes")

def load_maps(filename, left, top, right, bottom):
    width, height = right - left + 1, bottom - top + 1
    bitstring = "1" * width * height
    intmap = [0 for x in range(width * height)]
    file = open(filename, 'rb')
    i = 1
    while not file.closed:
        bx = file.read(2)
        by = file.read(2)
        x = int.from_bytes(bx, byteorder='little', signed=True)
        y = int.from_bytes(by, byteorder='little', signed=True)
        if bx == b'' or by == b'':
            file.close()
        else:
            px, py = x - left, y - top
            pos = px + (width * py)
            bitstring = bitstring[0:pos] + "0" + bitstring[pos+1:]
            intmap[pos] = i % 256
        i = i + 1
    return bitstring, intmap

def read_things(bytemap):
    pairs = []
    left, top, right, bottom = 0, 0, 0, 0
    for i in range(0, len(bytemap), 2):
        x = int.from_bytes(bytemap[i: i + 2], byteorder='little', signed=True)
        y = int.from_bytes(bytemap[i + 2: i + 4], byteorder='little', signed=True)
        angle = bytemap[i + 4: i + 6]
        type = bytemap[i + 6: i + 8]
        flags = bytemap[i + 8: i + 10]
        pairs.append((x, y))
        if x < left: left = x
        if x > right: right = x
        if y < top: top = y
        if y > bottom: bottom = y
    return pairs

def read_vertices(bytemap):
    pairs = []
    left, top, right, bottom = 0, 0, 0, 0
    for i in range(0, len(bytemap), 4):
        bx = bytemap[i:i+2]
        by = bytemap[i+2:i+4]
        x = int.from_bytes(bx, byteorder='little', signed=True)
        y = int.from_bytes(by, byteorder='little', signed=True)
        pairs.append((x, y))
        if x < left: left = x
        if x > right: right = x
        if y < top: top = y
        if y > bottom: bottom = y
    return pairs, (left, top, right, bottom)

def scale(div):
    width, height = int(65536 / div), int(65536 / div)
    origin = int(65536 / div / 2)
    return width, height, origin

def save_bitmap(bitmap, width, height, name):
    with open(name + ".pbm", 'wb') as file:
        file.write(b"P4 ")
        file.write(bytes(str(width) + " ", 'utf_8'))
        file.write(bytes(str(height) + " ", 'utf_8'))
        bytemap = bytearray()
        for i in range(0, len(bitmap), 8):
            bytemap.append(int(bitmap[i:i+8], 2))
        file.write(bytemap)

def save_graymap(bitmap, width, height, name):
    with open(name + ".pgm", 'wb') as file:
        file.write(b"P5 ")
        file.write(bytes(str(width) + " ", 'utf_8'))
        file.write(bytes(str(height) + " ", 'utf_8'))
        file.write(b"255 ")
        for b in bitmap:
            file.write(b.to_bytes(1, 'little'))

if __name__ == "__main__":
    try: main()
    except KeyboardInterrupt: print("Keyboard Interrupt (Control-C)...")
    sys.exit()
