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
import sys

# TODO: Patcher works with lump formats and should not open a WAD by 
# itself. It should invoke Wadder functions for that purpose, otherwise 
# work only with '.lmp' files directly.
def main():
    filename = sys.argv[-1]
    header = get_header(filename)

def get_header(filename):
    with open(filename, 'rb') as file:
        width = int.from_bytes(file.read(2), byteorder='little')
        height = int.from_bytes(file.read(2), byteorder='little')
        leftoffset = int.from_bytes(file.read(2), byteorder='little')
        topoffset = int.from_bytes(file.read(2), byteorder='little')
        columnofs = int.from_bytes(file.read(4 * (width%256)), byteorder='little')
    print("width:", width)
    print("height:", height)
    print("leftoffset:", leftoffset)
    print("topoffset:", topoffset)
    print("columnoffset:", columnofs)
    if width > 256:
        print("patcher: width was truncated to 256")
        print("patcher: this file is likely not a patch lump")

if __name__ == "__main__":
    try: main()
    except KeyboardInterrupt: print("Keyboard Interrupt (Control-C)...")
    sys.exit()
