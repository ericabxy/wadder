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

from xwadder import Doom

def main():
    if len(sys.argv) > 1:
        filename = sys.argv[1]
    else:
        print("usage: python patter.py [filename] [arguments]")
    if os.path.isfile(filename):
        with open(filename, 'rb') as file:
            data = file.read()
            picture = Doom.Picture(data)
        for arg in sys.argv:
            if arg[0: 10] == "--playpal=":
                path = arg[10:]
                with open(path, 'rb') as file:
                    playpal = Doom.Playpal(file.read())
            elif arg == "--save-pixmap":
                palette = playpal.maps[0]
                name = os.path.splitext(filename)[0] + ".ppm"
                palette = playpal.get_translate('brown')
                picture.save_pixmap(palette, name)
            elif arg == "--save-graymap":
                name = os.path.splitext(filename)[0] + ".pgm"
                picture.save_graymap(name)
            elif arg[0: 14] == "--save-pixmap=":
                name = arg[14:]
                palette = playpal.maps[0]
                picture.save_pixmap(palette, name)
            elif arg[0: 15] == "--save-graymap=":
                name = arg[15:]
                picture.save_graymap(name)

if __name__ == "__main__":
    try: main()
    except KeyboardInterrupt: print("Keyboard Interrupt (Control-C)...")
    sys.exit()
