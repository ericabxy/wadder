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
"""Perform operations on a WAD file.

Usage: main.py [filename] [arguments]

'filename' is used to load a WAD file and the following arguments
operate on the WAD.

--find=[string]

    Print every entry named beginning with 'string'.

--list=[N]

    Print the metadata for N entries.

--save-lump=[N]

    Save Nth lump as a raw '.lmp' file.

--save-map=[name]

    Find a map named 'name' and save each map lump to a folder.

--save-patch=[N]

    Try to save Nth lump as a raster image file.

--start=[N]

    Set the starting point for '--list='.
"""
import os
import sys
import tempfile

from xwadder import patch, wads, Doom

def _main():
    if len(sys.argv) > 1:
        path = sys.argv[1]
        if os.path.isfile(path):
            wad = wads.Wad(path)
            if len(sys.argv) > 2:
                _parse(wad, sys.argv)

def _parse(wad, args):
    start = 0  # start at index 0 by default
    for arg in args:
        if arg[0: 7] == "--find=":
            name = arg[7: ]
            index, x = wad.locate(name), 0
            while isinstance(index, int):
                entry = wad.get_entry(index)
                print(entry)
                x = x + 1
                index = wad.locate(name, x)
        elif arg[0: 7] == "--list=":
            number = int(arg[7: ])
            stop = start + int(number)
            for n in range(start, stop):
                entry = wad.get_entry(n)
                print(entry)
        elif arg[0: 12] == "--save-lump=":
            n = int(arg[12: ])
            data = wad.get_lump(n)
            entry = wad.get_entry(n)
            name = "".join([entry['name'], ".lmp"])
            with open(name, 'wb') as file:
                print("saving lump data to", name)
                file.write(data)
        elif arg[0: 11] == "--save-map=":
            name = arg[11: ]
            if not os.path.isdir(name):
                os.mkdir(name)
            locate = wad.locate_name(name)
            for n in range(locate, locate + 11):
                entry = wad.get_entry(n)
                data = wad.get_lump(n)
                path = os.path.join(name, entry['name'])
                with open(path, 'wb') as file:
                    file.write(data)
        elif arg[0: 13] == "--save-patch=":
            n = int(arg[13: ])
            data = wad.get_lump(n)
            entry = wad.get_entry(n)
            name = ".".join([entry['name'], "lmp"])
            with tempfile.TemporaryFile('r+b') as file:
                file.write(data)
                picture = patch.Picture(file)
            number = wad.locate_name("PLAYPAL")
            if number:
                playpal = wad.get_lump(number)
            name = ".".join([entry['name'], "ppm"])
            picture.save_image(name, playpal)
        elif arg[0: 8] == "--start=":
            start = int(arg[8: ])

if __name__ == "__main__":
    try: _main()
    except KeyboardInterrupt: print("Keyboard Interrupt (Control-C)...")
    sys.exit()
