#!/usr/bin/env python3
"""Paller - a module for working with 256-color palettes
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
        index = 0
        for arg in sys.argv:
            if arg[0:11] == "--save-pal=":
                index = int(arg[11:])
                with open(filename, 'rb') as file:
                    file.seek(index*768)
                    pal = file.read(768)
                save_lump(pal, "pal" + str(index) + ".lmp")
                save_palmap(pal, "pal" + str(index) + ".ppm")
            elif arg[0:7] == "--lump=":
                lumpname = arg[7:]
                print("paller: reading", lumpname, "for color mapping")
                with open(lumpname, 'rb') as file:
                    bytemap = file.read()
                if "--save-pixmap" in sys.argv:
                    with open(filename, 'rb') as file:
                        pixels = []
                        origin = index * 768
                        for b in bytemap:
                            offset = b * 3
                            file.seek(origin + offset)
                            pixels.append(file.read(3))
                    name = os.path.splitext(lumpname)[0]
                    print("paller: saving remapped pixels to", name + ".ppm")
#                    save_graymap(bytemap, name + ".pgm")
                    save_pixmap(pixels, name + ".ppm")
            elif arg[0:10] == "--palette=":
                index = int(arg[10:])
                print("paller: selecting palette", index, "from", filename)
        if os.path.getsize(filename)%768 == 0:
            pals = os.path.getsize(filename)//768
            with open(filename, 'rb') as file:
                if "--file-lumps" in sys.argv:
                    for p in range(pals):
                        print("paller: saving values to pal" + str(p) + ".lmp")
                        saveas_lump(file, "pal" + str(p) + ".lmp")
                elif "--file-hexmaps" in sys.argv:
                    for p in range(pals):
                        print("paller: saving values to pal" + str(p) + ".txt")
                        saveas_text(file, "pal" + str(p) + ".txt")
    else:
        print("paller: not a file '" + filename + "'")

def check_file(filename):
    print("paller: filename", filename)
    filesize = os.path.getsize(filename)
    if filesize == 10752:
        print("paller: filesize", filesize, "is likely a PLAYPAL lump")
        print("paller:", filesize//768, "palette(s) detected")
    elif filesize%768 == 0:
        print("paller: filesize", filesize, "may be an RGB palette lump")
        print("paller:", filesize//768, "palette(s) detected")
    else:
        print("paller: filesize", filesize)
        print("paller: this is likely not a palette lump")

def save_graymap(bytemap, name):
    """Save bytes to a 4096-pixel Portable GrayMap."""
    with open(name, 'wb') as file:
        file.write(b"P5 ")
        file.write(b"64 64 ")
        file.write(b"255 ")
        file.write(bytemap)

def save_lump(bytes, name):
    """Save palette as lump data."""
    with open(name, 'wb') as file:
        file.write(bytes)

def saveas_lump(file, name):
    """Save palette as lump data."""
    with open(name, 'wb') as fout:
        for i in range(256):
            color = file.read(3)
            fout.write(color)

def save_palmap(pixmap, name):
    """Save remapped bytes to a Portable PixMap file."""
    with open(name, 'wb') as file:
        file.write(b"P6 ")
        file.write(b"16 16 ")
        file.write(b"255 ")
        file.write(pixmap)

def save_pixmap(pixels, name):
    """Save remapped bytes to a Portable PixMap file."""
    with open(name, 'wb') as file:
        file.write(b"P6 ")
        file.write(b"64 64 ")
        file.write(b"255 ")
        for pixel in pixels:
            file.write(pixel)

def saveas_pixmap(file, name):
    """Save a palette to a Portable PixMap file.

    Paller saves each color in the palette as a pixel in the image.
    """
    with open(name, 'wb') as fout:
        fout.write(b"P6 ")
        fout.write(b"16 16 ")
        fout.write(b"255 ")
        for i in range(256):
            color = file.read(3)
            fout.write(color)

def saveas_text(file, name):
    """Save the color information as hex values."""
    with open(name, 'w') as fout:
        for i in range(256):
            color = file.read(3)
            fout.write(color.hex() + "\n")

if __name__ == "__main__":
    try: main()
    except KeyboardInterrupt: print("Keyboard Interrupt (Control-C)...")
    sys.exit()

