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
"""Work with lumps associated with a level map
"""

class Level:
    def __init__(self, **lumps):
        self.lumps = {}
        for name, lump in lumps.items():
            self.lumps[name] = lump

    def add_lump(self, name, lump):
        """Add a lump to the dictionary."""
        self.lumps[name] = lump

    def save_wad(self):
        """Save all lumps in a new 'header.wad'."""

    def save_folder(self):
        """Save all lumps individually in 'folder'."""
