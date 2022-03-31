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
"""
a module for working with WAD files and content

The 'Wad' class encapsulates metadata from a WAD file and provides
methods to retrieve lump data.

'readint' and 'readstr' functions interpret binary data in a standard
way.
"""
import os
import sys

class Wad:
    """Represent a WAD binary data file.

    This object is data-agnostic. It knows how to interpret the file's
    header and directory, read lump names, extract lump data, etc. but
    cannot interpret lump data.

    'directory' is the list of metadata about lumps.

    'entry' is the metadata for one lump in dictionary form.

    'lump' is the raw binary data in bytes form.
    """

    def __init__(self, filename):
        """Construct header and directory from WAD file.

        First load and interpret the 12-byte header. If the header
        indicates a valid WAD format, load and interpret the directory.
        """
        self.byteorder = 'little'
        with open(filename, 'rb') as file:
            self.header = file.read(12)
            file.seek(0)
            self.identification = readstr(file.read(4))
            self.numlumps = readint(file.read(4))
            self.infotableofs = readint(file.read(4))
            if self.identification[1:] == "WAD":
                self.directory = []
                file.seek(self.infotableofs)
                for i in range(self.numlumps):
                    filepos = readint(file.read(4))
                    size = readint(file.read(4))
                    name = readstr(file.read(8))
                    entry = dict(
                            index=i,
                            filepos=filepos,
                            size=size,
                            name=name)
                    self.directory.append(entry)
        self.filename = filename

    def locate(self, name, n=0):
        """Return the location of the nth entry matching 'name'."""
        instances = []
        for i, entry in enumerate(self.directory):
            if entry['name'][:len(name)] == name:
                instances.append(i)
        if len(instances) > n:
            return instances[n]

    def locate_name(self, name, multi=False):
        """Return the location of the first entry matching 'name'."""
        locates = []
        for i, entry in enumerate(self.directory):
            if entry['name'][:len(name)] == name:
                if multi:
                    locates.append(i)
                else:
                    return i
        return locates

    def get_entry(self, index):
        """Return the entry at 'index'."""
        return self.directory[index]

    def get_lump(self, index):
        """Return lump data as bytes."""
        entry = self.directory[index]
        with open(self.filename, 'rb') as file:
            file.seek(entry['filepos'])
            lump = file.read(entry['size'])
        return lump

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


def readint(data):
    """Interpret binary data as an integer."""
    return int.from_bytes(data, byteorder='little')

def readstr(data):
    """Interpret binary data as a string."""
    return data.decode('ascii').strip("\0")
