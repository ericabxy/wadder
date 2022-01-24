#!/usr/bin/env python3
"""
Patter - a script for working with the DOOM picture format
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
        header, columns = load_patch(filename)
        colormap = graymap()
        for arg in sys.argv:
            if arg[0:11] == "--colormap=":
                path = arg[11:]
                colormap = load_colormap(path)
            elif arg == "--save-pixmap":
                bytemap, bitmask = get_bytemap(header, columns)
                pixmap = get_pixmap(bytemap, bitmask, colormap)
                name = os.path.splitext(filename)[0] + ".ppm"
                save_pixmap(pixmap, header['width'], header['height'], name)

def get_bytemap(header, columns):
    width, height = header['width'], header['height']
    bytemap = bytearray(width * height)
    bitmask = [0 for i in range(width * height)]
    for i, column in enumerate(columns):
        for post in column:
            topdelta = post['topdelta']
            for j, data in enumerate(post['data']):
                bytemap[i + (topdelta * width) + (j * width)] = data
                bitmask[i + (topdelta * width) + (j * width)] = 1
    return bytemap, bitmask

def get_pixmap(bytemap, bitmask, colormap):
    pixmap = bytearray()
    for b, m in zip(bytemap, bitmask):
        if m == 0:
            pixmap.extend((255, 0, 255))
        else:
            pixmap.extend((colormap[b*3], colormap[b*3+1], colormap[b*3+2]))
    return pixmap

def graymap():
    map = bytearray()
    for i in range(256):
        map.extend((i, i, i))
    return map

def load_colormap(filename):
    """Load a 24bpp color translation map."""
    with open(filename, 'rb') as file:
        return file.read(768)

def load_patch(filename, maxw=256):
    """Return each part of the file header in a dictionary."""
    with open(filename, 'rb') as file:
        width = int.from_bytes(file.read(2), byteorder='little')
        height = int.from_bytes(file.read(2), byteorder='little')
        leftoffset = int.from_bytes(file.read(2), byteorder='little')
        topoffset = int.from_bytes(file.read(2), byteorder='little')
        columnofs = []
        for i in range(width % maxw):
            columnofs.append(int.from_bytes(file.read(4), byteorder='little'))
    header = dict(width=width,height=height,leftoffset=leftoffset,
                  topoffset=topoffset,columnofs=columnofs)
    if width > maxw:
        print("patter: WARNING width >", maxw, "likely not a patch lump")
    with open(filename, 'rb') as file:
        columns = []  # array to hold picture columns
        for i, offset in enumerate(columnofs):
            file.seek(offset)
            topdelta = 0
            posts = []  # array to hold posts in column
            while topdelta < 255:  # read posts until terminator
                topdelta = int.from_bytes(file.read(1), byteorder='little')
                length = int.from_bytes(file.read(1), byteorder='little')
                unused1 = int.from_bytes(file.read(1), byteorder='little')
                data = file.read(length)
                unused2 = int.from_bytes(file.read(1), byteorder='little')
                if topdelta < 255:
                    posts.append(dict(topdelta=topdelta,data=data))
            columns.append(posts)
    return header, columns

def save_pixmap(bytemap, width, height, name):
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
