#!/usr/bin/env python3
"""
Wads - a module for working with generic WAD and lump files
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
    # user-friendly checks and output
    args = sys.argv
    if len(args) < 2:
        usage()
        sys.exit()
    elif "--help" in args:
        help()
        sys.exit()
    elif os.path.isfile(args[-1]):
        filename = args[-1]
    else:
        sys.exit()
    header = get_header(filename)
    directory = get_directory(filename,
                              header['infotableofs'],
                              header['numlumps'])
    datakeys = ["filepos", "size", "name"]
    # print any header information requested
    for key in header.keys():
        if "--header-" + key in sys.argv:
            print(header[key])
    # process all command flags in order
    # TODO: what if "directory" does not exist?
    index, endex = 0, len(directory)-1
    for arg in sys.argv:
        if arg[0:7] == "--data=":
            key = arg[7:]
            if key not in datakeys:
                datakeys.append(key)
        elif arg[0:12] == "--data-only=":
            datakeys = [arg[12:]]
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
                    if "--indexed" in sys.argv:
                        print(i, end=": ")
                    for data in get_data(entry, datakeys):
                        print(data, end=" ")
                    print()
                    if "--save" in args:
                        lump = get_lump(filename, entry)
                        save_lump(lump, entry['name'])
        elif arg[0:8] == "--index=":
            index = int(arg[8:])
        elif arg == "--length":
            print(len(directory))
        elif arg == "--list":
            for i in range(index, endex+1):
                entry = directory[i]
                if "--indexed" in args:
                    print(i, end=": ")
                for data in get_data(entry, datakeys):
                    print(data, end=" ")
                print()
                if "--save" in args:
                    lump = get_lump(filename, entry)
                    save_lump(lump, entry['name'])
        elif arg[0:7] == "--save=":
            index = int(arg[7:])
            entry = directory[index]
            lump = get_lump(filename, entry)
            save_lump(lump, entry['name'])
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
        print_header(header)

def get_data(entry, keys):
    """Return a list of data from one entry."""
    datalist = []
    for key in keys:
        if key in entry:
            datalist.append(entry[key])
    return tuple(datalist)

def get_directory(filename, offset, numlumps):
    """Return the directory as a list of dictionaries."""
    directory = []
    with open(filename, 'rb') as file:
        if file.read(4)[1:4] == b"WAD":
            file.seek(offset)
            for i in range(numlumps):
                filepos = int.from_bytes(file.read(4), byteorder='little')
                size = int.from_bytes(file.read(4), byteorder='little')
                name = file.read(8).decode('ascii')
                entry = dict(
                        index=str(i)+":",
                        filepos=filepos,
                        size=size,
                        name=name)
                directory.append(entry)
    return tuple(directory)

def get_header(filename):
    """Return each part of the file header in a dictionary."""
    with open(filename, 'rb') as file:
        bytemap = file.read(12)
    header = {'bytes': bytemap}
    if bytemap[0:4].decode() == "IWAD":
        header['type'] = "Internal WAD"
    elif bytemap[0:4].decode() == "PWAD":
        header['type'] = "Patch WAD"
    elif bytemap[1:4].decode() == "WAD":
        header['type'] = "nonstandard"
    else:
        header['type'] = "not a WAD"
    header['identification'] = bytemap[0:4].decode()
    header['numlumps'] = int.from_bytes(bytemap[4:8], 'little')
    header['infotableofs'] = int.from_bytes(bytemap[8:12], 'little')
    return header

def get_lump(filename, entry):
    """Return lump data as binary data."""
    name = entry['name'].rstrip("\0") + ".lmp"
    with open(filename, 'rb') as file:
        file.seek(entry['filepos'])
        lump = file.read(entry['size'])
    return lump

def print_header(header):
    """Print header information in a human-readable way."""
    print("raw header:", header['header'])
    print("signature:", header['identification'])
    print("total number of lumps:", header['numlumps'])
    print("location of directory:", header['infotableofs'])

def save_lump(data, name, ext=".lmp"):
    filename = name.rstrip("\0") + ext
    print("wadder: saving lump data to binary file", filename)
    with open(filename, 'w+b') as file:
        file.write(data)

class Wad:
    def __init__(self, filename):
        self.byteorder = 'little'
        with open(filename, 'rb') as file:
            if file.peek(4)[1:4] == b"WAD":
                print("WARNING: WAD signature not recognized")
                print("raw signature", file.peek(4)[1:4])
            self.read_header(file)
            self.read_directory(file)

    def read_directory(self, file):
        directory = []
        file.seek(self.infotableofs)
        for i in range(numlumps):
            filepos = self.readint(file.read(4))
            size = self.readint(file.read(4))
            name = file.read(8).decode('ascii')
            entry = dict(
                    index=str(i)+":",
                    filepos=filepos,
                    size=size,
                    name=name)
            directory.append(entry)
        self.directory = tuple(directory)

    def read_header(self, file):
        self.header = file.peek(12)
        self.ident = self.readstr(file.read(4))
        self.nlumps = self.readint(file.read(4))
        self.infotableofs = self.readint(file.read(4))

    def readint(self, data):
        return int.from_bytes(data, byteorder=self.byteorder)

    def readstr(self, data):
        return data.decode()


if __name__ == "__main__":
    try: main()
    except KeyboardInterrupt: print("Keyboard Interrupt (Control-C)...")
    sys.exit()
