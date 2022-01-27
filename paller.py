#!/usr/bin/env python3
"""
Paller - a module for working with binary truecolor palettes
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
        playpal = load_playpal(filename, index)
        for arg in sys.argv:
            if arg[0:8] == "--index=":
                index = int(arg[8:])
                print("paller: using palette", index)
                playpal = load_playpal(filename, index)
            elif arg == "--print":
                for i in range(0, 768, 3):
                    print(playpal[i:i+3].hex())
            elif arg[0:7] == "--save-":
                name = os.path.splitext(filename)[0] + str(index)
                if arg == "--save-hexmap":
                    print("paller: saving hex values to", name + ".txt")
                    save_hexmap(playpal, name + ".txt")
                if arg == "--save-lump":
                    print("paller: saving lump data to", name + ".lmp")
                    save_lump(playpal, name + ".lmp")
                if arg == "--save-pixmap" in sys.argv:
                    print("paller: saving colors to", name + ".ppm")
                    save_pixmap(playpal, name + ".ppm")
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

def load_playpal(filename, index):
    with open(filename, 'rb') as file:
        file.seek(768 * index)
        playpal = file.read(768)
    return playpal

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

def save_lump(bytemap, name):
    """Save palette as lump data."""
    with open(name, 'wb') as file:
        file.write(bytemap)

def save_pixmap(playpal, name):
    """Save remapped bytes to a Portable PixMap file."""
    with open(name, 'wb') as file:
        file.write(b"P6 ")
        file.write(b"16 16 ")
        file.write(b"255 ")
        for i in range(0, 768, 3):
            color = playpal[i:i+3]
            file.write(color)

def save_hexmap(playpal, name):
    """Save each color value in hexadecimal."""
    with open(name, 'w') as file:
        for i in range(0, 768, 3):
            name = playpal[i:i+3].hex()
            file.write(name + "\n")

if __name__ == "__main__":
    try: main()
    except KeyboardInterrupt: print("Keyboard Interrupt (Control-C)...")
    sys.exit()

