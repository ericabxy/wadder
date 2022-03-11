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
Wadder - modules for handling the WAD file format.

Using some of the extensive documentation found at The Doom Wiki[1],
Wadder provides functions and classes designed to interpret and extract
binary data from files in WAD format. Generic modules can find and
extract the lumps from a WAD, while more specialized modules can parse
the binary data contained in generalized lumps. Game-specific modules
can interpret the data from specialized lumps.

MODULES

wads - read and extract binary data from WAD files

levels - collect and save multiple lumps as level data

Doom - interpret lumps formatted for the Doom engine

FOOTNOTES

According to the Doom Bible, WAD is an acronym for "Where's All the
Data?". Alternatively, Wadder considers "Wad of Aggregate Data" to be
an appropriate backronym.

1: https://doomwiki.org/
"""
