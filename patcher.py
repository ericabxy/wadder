#!/usr/bin/env python3
"""Patcher - a script for working with DOOM picture format
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
    if os.path.isfile(sys.argv[-1]):
        check_file(sys.argv[-1])

def check_file(filename):
    with open(filename, 'rb') as file:
        width = int.from_bytes(file.read(2), byteorder='little')
        height = int.from_bytes(file.read(2), byteorder='little')
        leftoffset = int.from_bytes(file.read(2), byteorder='little')
        topoffset = int.from_bytes(file.read(2), byteorder='little')
        columnofs = []
        for i in range(width % 256):
            columnofs.append(int.from_bytes(file.read(4), byteorder='little'))
    print("width:", width)
    print("height:", height)
    print("leftoffset:", leftoffset)
    print("topoffset:", topoffset)
    print("columnofs:", end=" ")
    for ofs in columnofs:
        print(ofs, end=" ")
    print()
    bytemap = bytearray(width*height)
    colormap = load_hexmap("data/pal0.txt")
    xhexmap = ['ff00ff' for i in range(width*height)]
    with open(filename, 'rb') as file:
        for i, offset in enumerate(columnofs):
            print("column:", i)
            file.seek(offset)
            topdelta = 0
            while topdelta < 255:
                topdelta = int.from_bytes(file.read(1), byteorder='little')
                length = int.from_bytes(file.read(1), byteorder='little')
                unused1 = int.from_bytes(file.read(1), byteorder='little')
                data = file.read(length)
                unused2 = int.from_bytes(file.read(1), byteorder='little')
                print("  topdelta:", topdelta)
                for j in range(length):
#                    print(i, end=" ")
#                    print(topdelta*256, end=" ")
#                    print(j*256)
                    if topdelta < 255:
                        color = data[j]
                        bytemap[i+(topdelta*width)+(j*width)] = color
                        hex = colormap[color]
                        xhexmap[i+(topdelta*width)+(j*width)] = hex
#                print("  length:", length)
#                print("  data:", data)
    name = os.path.splitext(filename)[0]
    save_graymap(bytemap, name + ".pgm", width, height)
    save_pixmap(xhexmap, name + ".ppm", width, height)
    if width > 256:
        print("patcher: width was truncated to 256")
        print("patcher: this file is likely not a patch lump")

def load_hexmap(filename):
    """Return 256 hex-encoded values read from a file."""
    map = []
    with open(filename) as file:
        for i in range(256):
            map.append(file.readline())
    return map

def save_graymap(bytemap, name, width=256, height=256):
    """Save bytes to a Portable GrayMap."""
    with open(name, 'wb') as file:
        file.write(b"P5 ")
        file.write(bytes(str(width) + " ", 'utf_8'))
        file.write(bytes(str(height) + " ", 'utf_8'))
        file.write(b"255 ")
        file.write(bytemap)

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
