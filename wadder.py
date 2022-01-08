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
import sys

def main():
    filename = sys.argv[-1]
    if len(sys.argv) > 2: argcmd = sys.argv[1]
    else: argcmd = ""
    if len(sys.argv) > 3: argnum = int(sys.argv[2])
    else: argnum = 0
    header = get_header(filename)
    directory = get_directory(filename,
                              header['infotableofs'],
                              header['numlumps'])
    if argcmd == "--entry":
        entry = directory[argnum]
        for value in entry.values():
            print(value, end=" ")
        print()
    elif argcmd in ("--filepos", "--name", "--size"):
        entry = directory[argnum]
        print(entry[argcmd[2:]])
    elif argcmd[0:7] == "--find=":
        match = argcmd[7:]
        for i, entry in enumerate(directory):
            if entry['name'][:len(match)] == match:
                print(str(i) + ":", end=" ")
                for value in entry.values():
                    print(value, end=" ")
                print()
    elif argcmd == "--header":
        pass
    elif argcmd == "--length":
        print(len(directory))
    elif argcmd in ("--list", "--indexed-list"):
        for i, entry in enumerate(directory):
            if argcmd == "--indexed-list":
                print(i, end=": ")
            for value in entry.values():
                print(value, end=" ")
            print()
    elif argcmd[0:7] == "--list=":
        start = int(argcmd[7:])
        stop = argnum+1
        for i in range(start, stop):
            entry = directory[i]
            if argcmd[0:15] == "--indexed-list=":
                print(i, end=": ")
            for value in entry.values():
                print(value, end=" ")
            print()
    elif argcmd == "--save":
        entry = directory[argnum]
        save_lump(filename, entry['filepos'], entry['size'], entry['name'])
    else:
        print("wadder: raw header", header['raw'])
        if header['raw'][0:4] == b"IWAD":
            print("wadder: 'Internal WAD' signature identified")
        elif header['raw'][0:4] == b"PWAD":
            print("wadder: 'Patch WAD' signature identified")
        elif header['raw'][1:4] == b"WAD":
            print("wadder: non-standard WAD signature")
        else:
            print("wadder: file does not have a WAD signature")
        print_header(header)

def print_header(header):
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
                name = file.read(8).decode()
                entry = dict(filepos=filepos,size=size,name=name)
                directory.append(entry)
            return tuple(directory)

def get_header(filename):
    with open(filename, 'rb') as file:
        header = file.read(12)
    ident = header[0:4].decode()
    nlumps = int.from_bytes(header[4:8], byteorder='little')
    offs = int.from_bytes(header[8:12], byteorder='little')
    return dict(identification=ident,numlumps=nlumps,infotableofs=offs,raw=header)

def save_lump(filename, filepos, size, name):
    name = name + ".binary"
    print("wadder: saving lump data to binary file", name)
    with open(filename, 'rb') as file:
        file.seek(filepos)
        lump = file.read(size)
        newfile = open(name, 'w+b')
        newfile.write(lump)
        newfile.close()

if __name__ == "__main__":
    try: main()
    except KeyboardInterrupt: print("Keyboard Interrupt (Control-C)...")
    sys.exit()
