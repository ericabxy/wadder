#!/usr/bin/env python3
"""Patter - a script for working with DOOM picture format
Copyright 2022 Eric Duhamel

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>."""
import os
import sys

def main():
    filename = sys.argv[-1]
    if os.path.isfile(filename):
        if len(sys.argv) < 3:
            check_file(filename)
        colormap = graymap()
        for arg in sys.argv:
            if arg[0:14] == "--read-hexmap=":
                path = arg[14:]
                colormap = read_hexmap(path)
            elif arg == "--save-pixmap":
                picture, width, height = load_picture(filename, colormap)
                name = os.path.splitext(filename)[0]
                save_pixmap(picture, name + ".ppm", width, height)

def check_file(filename, maxw=256):
    with open(filename, 'rb') as file:
        width = int.from_bytes(file.read(2), byteorder='little')
        height = int.from_bytes(file.read(2), byteorder='little')
        leftoffset = int.from_bytes(file.read(2), byteorder='little')
        topoffset = int.from_bytes(file.read(2), byteorder='little')
        columnofs = []
        for i in range(width % maxw):
            columnofs.append(int.from_bytes(file.read(4), byteorder='little'))
    print("width:", width)
    print("height:", height)
    print("leftoffset:", leftoffset)
    print("topoffset:", topoffset)
    print("columnofs:", end=" ")
    for ofs in columnofs:
        print(ofs, end=" ")
    print()
    if width > maxw:
        print("patter: width greater than", maxw, "limit; aborting")
    else:
        with open(filename, 'rb') as file:
            for i, offset in enumerate(columnofs):
                print("column:", i)
                file.seek(offset)
                topdelta = 0
                while topdelta < 255:  # read posts until terminator
                    topdelta = int.from_bytes(file.read(1), byteorder='little')
                    length = int.from_bytes(file.read(1), byteorder='little')
                    unused1 = int.from_bytes(file.read(1), byteorder='little')
                    data = file.read(length)
                    unused2 = int.from_bytes(file.read(1), byteorder='little')
                    if topdelta < 255:
                        print("  topdelta:", topdelta)
                        print("  length:", length)
                        for j in range(length):
                            if topdelta < 255:
                                print("    post", j, end=": ")
                                print(bin(data[j])[2:])

def get_header(filename):
    """Return each part of the file header in a dictionary."""
    with open(filename, 'rb') as file:
        width = int.from_bytes(file.read(2), byteorder='little')
        height = int.from_bytes(file.read(2), byteorder='little')
        leftoffset = int.from_bytes(file.read(2), byteorder='little')
        topoffset = int.from_bytes(file.read(2), byteorder='little')
        columnofs = []
        for i in range(width % 256):
            columnofs.append(int.from_bytes(file.read(4), byteorder='little'))
    return dict(width=width,height=height,leftoffset=leftoffset,
            topoffset=topoffset,columnofs=columnofs)

def graymap():
    """Return 256 hex-encoded grayscale values."""
    map = []
    for i in range(256):
        hexval = hex(i)[2:].zfill(2)
        map.append(hexval + hexval + hexval + "\n")
    return map

def load_picture(filename, hexmap):
    with open(filename, 'rb') as file:
        width = int.from_bytes(file.read(2), byteorder='little')
        height = int.from_bytes(file.read(2), byteorder='little')
        leftoffset = int.from_bytes(file.read(2), byteorder='little')
        topoffset = int.from_bytes(file.read(2), byteorder='little')
        columnofs = []
        for i in range(width % 256):
            columnofs.append(int.from_bytes(file.read(4), byteorder='little'))
        picture = ['ff00ff' for i in range(width*height)]
        for i, offset in enumerate(columnofs):
            file.seek(offset)
            topdelta = 0
            while topdelta < 255:  # read posts until terminator
                topdelta = int.from_bytes(file.read(1), byteorder='little')
                length = int.from_bytes(file.read(1), byteorder='little')
                unused1 = int.from_bytes(file.read(1), byteorder='little')
                data = file.read(length)
                unused2 = int.from_bytes(file.read(1), byteorder='little')
                for j in range(length):
                    if topdelta < 255:
                        color = hexmap[data[j]]
                        picture[i+(topdelta*width)+(j*width)] = color
    return picture, width, height

def read_hexmap(filename):
    """Return 256 hex-encoded values read from a file."""
    map = []
    with open(filename) as file:
        for i in range(256):
            map.append(file.readline())
    return map

def save_pixmap(hexmap, name, width=256, height=256):
    """Save 3-byte hex values to a Portable PixMap."""
    with open(name, 'wb') as file:
        file.write(b"P6 ")
        file.write(bytes(str(width) + " ", 'utf_8'))
        file.write(bytes(str(height) + " ", 'utf_8'))
        file.write(b"255 ")
        for hex in hexmap:
            file.write(bytes.fromhex(hex))

if __name__ == "__main__":
    try: main()
    except KeyboardInterrupt: print("Keyboard Interrupt (Control-C)...")
    sys.exit()
