#!/usr/bin/env python3
"""Wadder - a script for working with WAD and related file formats
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
    args = sys.argv
    if os.path.isfile(args[-1]):
        filename = args[-1]
    else:
        filename = None
    header = get_header(filename)
    directory = get_directory(filename,
                              header['infotableofs'],
                              header['numlumps'])
    # print any header information requested
    for key in header.keys():
        if "--" + key in args:
            print(header[key])
    # find all command flags and follow orders
    # TODO: what if "directory" does not exist?
    index, endex = 0, 0
    for arg in sys.argv:
        if arg[0:7] == "--data=":
            name = arg[7:]
            print(get_data(directory, index, name))
        elif arg[0:6] == "--end=":
            endex = int(arg[6:])
        elif arg[0:8] == "--entry=":
            index = int(arg[8:])
            entry = directory[index]
            for value in entry.values():
                print(value, end=" ")
            print()
        elif arg[0:7] == "--find=":
            match = arg[7:]
            for i, entry in enumerate(directory):
                if entry['name'][:len(match)] == match:
                    if "--indexed" in args:
                        print(i, end=":")
                    for value in entry.values():
                        print(value, end=" ")
                    print()
                    if "--save" in args:
                        save_lump(filename, entry)
        elif arg[0:8] == "--index=":
            index = int(arg[8:])
            endex = index
        elif arg == "--length":
            print(len(directory))
        elif arg == "--list-range":
            for i in range(index, endex+1):
                entry = directory[i]
                if "--indexed" in args:
                    print(i, end=": ")
                for value in entry.values():
                    print(value, end=" ")
                print()
                if "--save" in args:
                    save_lump(filename, entry)
        elif arg == "--list":
            for i, entry in enumerate(directory):
                if "--indexed" in args:
                    print(i, end=": ")
                for value in entry.values():
                    print(value, end=" ")
                print()
        elif arg[0:7] == "--save=":
            index = int(arg[7:])
            entry = directory[index]
            save_lump(filename, entry)
    # cordially parse results if no commands are given
    if len(sys.argv) < 3:
        if header['header'][0:4] == b"IWAD":
            print("wadder: 'Internal WAD' signature identified")
        elif header['header'][0:4] == b"PWAD":
            print("wadder: 'Patch WAD' signature identified")
        elif header['header'][1:4] == b"WAD":
            print("wadder: non-standard WAD signature")
        else:
            print("wadder: file does not have a WAD signature")
        parse_header(header)

def get_data(directory, index, name):
    """Return data for an entry in the directory

    The argument 'directory' must be a table of dictionaries and
    'index' must be an integer within the length of the directory.
    'name' may be any string, but an entry in a WAD directory
    normally only has 'filpos', 'size', and 'name' data."""
    entry = directory[index]
    if name in entry:
        return entry[name]
    else:
        return False

def parse_header(header):
    """Print header information in a human-readable way."""
    print("raw header:", header['header'])
    print("signature:", header['identification'])
    print("total number of lumps:", header['numlumps'])
    print("location of directory:", header['infotableofs'])

def get_directory(filename, offset, numlumps):
    with open(filename, 'rb') as file:
        if file.read(4)[1:4] == b"WAD":
            file.seek(offset)
            directory = []
            for i in range(numlumps):
                filepos = int.from_bytes(file.read(4), byteorder='little')
                size = int.from_bytes(file.read(4), byteorder='little')
                name = file.read(8).decode('ascii')
                entry = dict(filepos=filepos,size=size,name=name)
                directory.append(entry)
            return tuple(directory)

def get_header(filename):
    with open(filename, 'rb') as file:
        header = file.read(12)
    ident = header[0:4].decode()
    nlumps = int.from_bytes(header[4:8], byteorder='little')
    offs = int.from_bytes(header[8:12], byteorder='little')
    return dict(identification=ident,numlumps=nlumps,infotableofs=offs,header=header)

def save_lump(filename, entry):
    """Find and save a lump as a binary file.

    The file seek position, bytesize, and filename for the lump is taken
    from an entry dictionary like those generated by function
    'get_directory'."""
    name = entry['name'].rstrip("\0") + ".lmp"
    print("wadder: saving lump data to binary file", name)
    with open(filename, 'rb') as file:
        file.seek(entry['filepos'])
        lump = file.read(entry['size'])
        newfile = open(name, 'w+b')
        newfile.write(lump)
        newfile.close()

if __name__ == "__main__":
    try: main()
    except KeyboardInterrupt: print("Keyboard Interrupt (Control-C)...")
    sys.exit()
