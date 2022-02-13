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
                        intex=i,
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

def save_lump(data, name, ext=".lmp"):
    filename = name.rstrip("\0") + ext
    print("wadder: saving lump data to binary file", filename)
    with open(filename, 'w+b') as file:
        file.write(data)

class Wad:
    """Represent a WAD binary data file.

    This object is data-agnostic. It knows how to interpret the file's
    header and directory, read lump names, extract lump data, etc. but
    cannot interpret lump data.
    """

    def __init__(self, filename):
        self.byteorder = 'little'
        with open(filename, 'rb') as file:
            self.header = file.read(12)
            file.seek(0)
            if self.read_header(file):
                self.read_directory(file)
        self.filename = filename

    def find_lumps(self, name, more=1):
        """Search and return entries matching 'name'.

        'more' appends a range of entries after the first one found
        """
        lumps = []
        for i, entry in enumerate(self.directory):
            if entry['name'][:len(name)] == name:
                for j in range(more):
                    lumps.append(self.directory[i + j])
        return lumps

    def get_lump(self, entry):
        """Return lump data as binary data."""
        name = entry['name'].rstrip("\0") + ".lmp"
        with open(self.filename, 'rb') as file:
            file.seek(entry['filepos'])
            lump = file.read(entry['size'])
        return lump

    def get_lumpnum(self, index):
        """Return lump data as binary data."""
        entry = self.directory[index]
        name = entry['name'].rstrip("\0") + ".lmp"
        with open(self.filename, 'rb') as file:
            file.seek(entry['filepos'])
            lump = file.read(entry['size'])
        return lump

    def read_directory(self, file):
        directory = []
        file.seek(self.infotableofs)
        for i in range(self.numlumps):
            filepos = self.readint(file.read(4))
            size = self.readint(file.read(4))
            name = file.read(8).decode('ascii')
            entry = dict(
                    index=i,
                    filepos=filepos,
                    size=size,
                    name=name)
            directory.append(entry)
        self.directory = tuple(directory)

    def read_header(self, file):
        self.identification = self.readstr(file.read(4))
        self.numlumps = self.readint(file.read(4))
        self.infotableofs = self.readint(file.read(4))
        return self.identification[1:] == "WAD"

    def readint(self, data):
        return int.from_bytes(data, byteorder=self.byteorder)

    def readstr(self, data):
        return data.decode()

    def report(self):
        if self.header[0:4] == b"IWAD":
            print("wadder: 'Internal WAD' signature identified")
        elif self.header[0:4] == b"PWAD":
            print("wadder: 'Patch WAD' signature identified")
        elif self.header[1:4] == b"WAD":
            print("wadder: non-standard WAD signature")
        else:
            print("wadder: file does not have a WAD signature")
        print("raw header:", self.header)
        print("signature:", self.identification)
        print("total number of lumps:", self.numlumps)
        print("location of directory:", self.infotableofs)
