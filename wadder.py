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
    datakeys = ["filepos", "size", "name"]
    # print any header information requested
    for key in header.keys():
        if "--header-" + key in args:
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
                    if "--indexed" in args:
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
    with open(filename, 'rb') as file:
        if file.read(4)[1:4] == b"WAD":
            file.seek(offset)
            directory = []
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
        header = file.read(12)
    ident = header[0:4].decode()
    nlumps = int.from_bytes(header[4:8], byteorder='little')
    offs = int.from_bytes(header[8:12], byteorder='little')
    return dict(header=header,identification=ident,
                numlumps=nlumps,infotableofs=offs)

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

def help():
    print("--data=filepos")
    print("--data=size")
    print("--data=name")
    print("")
    print("\t\tAdd the specified key to the list of metadata to print for each")
    print("\t\tentry. By default for each entry Wadder will print all three")
    print("\t\tmetadata, so normally this is not needed. However it can be used")
    print("\t\tto re-add to the list of metadata if it was removed with")
    print("\t\t'--data-only='.")
    print("")
    print("--data-only=filepos")
    print("--data-only=size")
    print("--data-only=name")
    print("")
    print("\t\tClear the list of metadata to print for each entry, and replace")
    print("\t\tit with only the key specified. If more metadata is needed, use")
    print("\t\t'--data=' to add more to the list.")
    print("")
    print("--end=N")
    print("")
    print("\t\tSet the last entry to index (inclusive) when using '--list'.")
    print("\t\tDefaults to the last entry in the directory.")
    print("")
    print("--entry=N")
    print("")
    print("\t\tPrint all metadata for a single entry in the directory at index")
    print("\t\tN.")
    print("")
    print("--find=string")
    print("")
    print("\t\tFind and print the entry for any lumps which have a name")
    print("\t\tstarting with 'string'. Also save each matching lump if the")
    print("\t\t'--save' flag is set.")
    print("")
    print("--header-identification")
    print("--header-numlumps")
    print("--header-infotableofs")
    print("")
    print("\t\tPrint the requested header information.")
    print("")
    print("--index=N")
    print("")
    print("\t\tSet the first entry to index when using '--list'. Defaults to")
    print("\t\tthe first entry [0].")
    print("")
    print("--indexed")
    print("")
    print("\t\tPrepend each entry listed by printing its index before the")
    print("\t\tmetadata.")
    print("")
    print("--length")
    print("")
    print("\t\tPrint the length of the directory.")
    print("")
    print("--list")
    print("")
    print("\t\tPrint each entry in the directory starting with '--index=' and")
    print("\t\tending with '--end='. Each entry is printed on a new line with a")
    print("\t\t" " separator between each metadata. If the '--indexed' flag is")
    print("\t\tset, prepend each entry with its index in the directory. If the")
    print("\t\t'--save' flag is set, save each entry listed as a raw lump file.")
    print("")
    print("--save")
    print("")
    print("\t\tSave the lump data from each entry listed as a binary file with")
    print("\t\tthe '.lmp' extension.")
    print("")
    print("--save=N")
    print("")
    print("\t\tSave the lump data from the entry specified by N as a binary")
    print("\t\tfile with the '.lmp' extension.")

def usage():
    print("invoked: ", sys.argv[0])
    print("usage: python3 wadder.py <parameters> <filename>")
    print("examples:")
    print("  python3 wadder.py freedoom2.wad")
    print("    parse and print the WAD header information for freedoom2.wad")
    print("  python3 wadder.py --index=10 --end=20 --list freedm.wad")
    print("    print the metadata for each entry from 10 to 20 for freedm.wad")
    print("  python3 wadder.py --find=FLOOR --save Valiant.wad")
    print("    find and save every lump in Valiant.wad named FLOOR*")
    print("  python3 wadder.py --save=100 DOOM2.WAD")
    print("    save the 100th lump found in DOOM2.WAD")

if __name__ == "__main__":
    try: main()
    except KeyboardInterrupt: print("Keyboard Interrupt (Control-C)...")
    sys.exit()
