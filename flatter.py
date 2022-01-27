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
        colormap, height, width = graymap(), 64, 64
        for arg in sys.argv:
            if arg[0:9] == "--height=":
                height = int(arg[9:])
            elif arg[0:10] == "--playpal=":
                path = arg[10:]
                colormap = load_playpal(path)
            elif arg == "--save-graymap":
                flat = load_flat(filename)
                name = os.path.splitext(filename)[0]
                print("flatter: saving color values to", name + ".pgm")
                save_graymap(flat, name + ".pgm")
            elif arg == "--save-pixmap":
                flat = load_flat(filename)
                pixmap = get_pixmap(flat, colormap)
                name = os.path.splitext(filename)[0]
                print("flatter: saving colormapped values to", name + ".ppm")
                save_pixmap(pixmap, width, height, name + ".ppm")
            elif arg[0:8] == "--width=":
                width = int(arg[8:])
    else:
        print("flatter: not a file '" + filename + "'")

def check_file(filename):
    print("flatter: filename", filename)
    filesize = os.path.getsize(filename)
    if filesize == 4096:
        print("flatter: filesize", filesize, "may be a 'flat' lump")
    else:
        print("flatter: filesize", filesize, "likely not a 'flat' lump")

def get_pixmap(bytemap, colormap):
    """Render a pixmap using color values and a transparency mask."""
    pixmap = bytearray()
    for b in bytemap:
        pixmap.extend((colormap[b*3], colormap[b*3+1], colormap[b*3+2]))
    return pixmap

def graymap():
    """Return a 256-shade graymap to substitute a colormap."""
    map = bytearray()
    for i in range(256):
        map.extend((i, i, i))
    return map

def load_flat(filename):
    """Return 4096 bytes from a binary file."""
    with open(filename, 'rb') as file:
#        return file.read(4096)
        return file.read()

def load_playpal(filename):
    """Load a 24bpp color translation map."""
    with open(filename, 'rb') as file:
        return file.read(768)

def save_graymap(bytemap, name):
    """Save bytes to a 4096-pixel Portable GrayMap."""
    with open(name, 'wb') as file:
        file.write(b"P5 ")
        file.write(b"64 64 ")
        file.write(b"255 ")
        file.write(bytemap)

def save_pixmap(bytemap, width, height, name):
    """Save binary data to a Portable PixMap file."""
    with open(name, 'wb') as file:
        file.write(b"P6 ")
        file.write(bytes(str(width) + " ", 'utf_8'))
        file.write(bytes(str(height) + " ", 'utf_8'))
        file.write(b"255 ")
        file.write(bytemap)

if __name__ == "__main__":
    try: main()
    except KeyboardInterrupt: print("Keyboard Interrupt (Control-C)...")
    sys.exit()

