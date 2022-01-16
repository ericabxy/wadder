#!/usr/bin/env python3
"""Flatter - a module for working with 64x64-pixel "flat" lumps
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
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""
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
            elif arg == "--save-graymap":
                flat = load_flat(filename)
                name = os.path.splitext(filename)[0]
                print("flatter: saving color values to", name + ".pgm")
                save_graymap(flat, name + ".pgm")
            elif arg == "--save-pixmap":
                flat = load_flat(filename)
                name = os.path.splitext(filename)[0]
                print("flatter: saving colormapped values to", name + ".ppm")
                save_pixmap(flat, colormap, name + ".ppm")
    else:
        print("flatter: not a file '" + filename + "'")

def check_file(filename):
    print("flatter: filename", filename)
    filesize = os.path.getsize(filename)
    if filesize == 4096:
        print("flatter: filesize", filesize, "may be a 'flat' lump")
    else:
        print("flatter: filesize", filesize)
        print("flatter: this is likely not a 'flat' lump")

def graymap():
    """Return 256 hex-encoded grayscale values."""
    map = []
    for i in range(256):
        hexval = hex(i)[2:].zfill(2)
        map.append(hexval + hexval + hexval + "\n")
    return map

def load_flat(filename):
    """Return 4096 bytes from a binary file."""
    with open(filename, 'rb') as file:
        return file.read(4096)

def read_hexmap(filename):
    """Return 256 hex-encoded values read from a file."""
    map = []
    with open(filename) as file:
        for i in range(256):
            map.append(file.readline())
    return map

def save_graymap(bytemap, name):
    """Save bytes to a 4096-pixel Portable GrayMap."""
    with open(name, 'wb') as file:
        file.write(b"P5 ")
        file.write(b"64 64 ")
        file.write(b"255 ")
        file.write(bytemap)

def save_pixmap(bytemap, colormap, name):
    with open(name, 'wb') as file:
        file.write(b"P6 ")
        file.write(b"64 64 ")
        file.write(b"255 ")
        for byte in bytemap:
            print(byte, end="->")
            color = colormap[byte]
            print(bytes.fromhex(color))
            file.write(bytes.fromhex(color))

if __name__ == "__main__":
    try: main()
    except KeyboardInterrupt: print("Keyboard Interrupt (Control-C)...")
    sys.exit()

