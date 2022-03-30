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
"""Interpret lump data designed for Doom and Doom II.

Lumps are stored in several different binary formats. Some have header
data and others do not. The classes defined here are designed to
transform the data into named attributes, leaving the binary data
behind.

Picture format: takes binary data read from a 'patch' lump. Mostly
implemented.

Map format: takes data from several lumps to form a complete set of
level data. Can interpret and return the data in useful ways e.g. line
and sector data for drawing a representation of the map geometry. NOT
implemented.

[patch](https://doomwiki.org/wiki/Picture_format)
"""

def read_int(data):
    """Translate an signed byte sequence to number."""
    return int.from_bytes(data, byteorder='little', signed=True)

def read_str(data):
    """Tranlate an ascii-encoded byte sequence to string.

    Some Doom strings are padded with null bytes, which are ignored.
    """
    return data.decode('ascii').strip("\0")

def read_uint(data):
    """Translate an unsigned byte sequence to number."""
    return int.from_bytes(data, byteorder='little', signed=False)

def read_uint_array(data, size):
    array = []
    for x in range(0, len(data), size):
        value = int.from_bytes(data[x: x + size], byteorder='little',
                signed=False)
        array.append(value)
    return array

def read_uint32_t_array(data):
    array = []
    for x in range(0, len(data), 4):
        value = int.from_bytes(data[x: x + 4], byteorder='little', signed=False)
        array.append(value)
    return array

class Picture():
    """An image in the Doom picture format.

    Picture takes a 'bytes' object. Normal procedure is to extract bytes
    from a 'Wad' object using the lump extraction method. You can also
    read bytes from a lump file opened in 'rb' mode.

    This class may be given invalid or corrupted picture data which
    could result in an abnormally long 'columnofs' array or an
    infinitely looping 'posts' extraction, so safeguards are needed to
    prevent either outcome.
    """

    def __init__(self, bytemap):
        self.width = read_uint(bytemap[0: 2])
        self.height = read_uint(bytemap[2: 4])
        self.leftoffset = read_int(bytemap[4: 6])
        self.topoffset = read_int(bytemap[6: 8])
        safe_width = self.width % 256
        columns_length = 4 * safe_width
        self.columnofs = read_uint32_t_array(bytemap[8: 8 + columns_length])
        self.columns = []
        if self.width <= safe_width:
            self.columns = self.read_columns(bytemap)

    def read_columns(self, bytemap):
        """

        There is one 'column' in the array per pixel of width in the
        picture. A column in turn is an array of 'posts' that are read
        starting at an 'offset' into the binary data.
        """
        columns = []
        for i, offset in enumerate(self.columnofs):
            column = self.read_posts(bytemap[offset:])
            columns.append(column)
        return columns

    def read_posts(self, bytemap):
        """Read every 'post' of pixels in this column.

        This method should receive a slice of the lump data starting
        at the column offset. It works using index 0 as the origin.
        """
        x, posts = 0, []
        post = Post(bytemap[x:])
        while post.valid:
            posts.append(post)
            x = x + post.length + 4
            post = Post(bytemap[x:])
        return posts

    def get_raster(self):
        """Return pixel map and transparency mask from draw data.

        The picture format is drawn top-to-bottom, skipping areas of
        transparency. Since 'map' can only store solid colors,
        transparent pixels are stored in 'mask'.
        """
        width, height = self.width, self.height
        map = bytearray(width * height)
        mask = bytearray(width * height)
        for x, column in enumerate(self.columns):
            for post in column:
                topdelta = post.topdelta
                for y, data in enumerate(post.data):
                    map[x + (topdelta * width) + (y * width)] = data
                    mask[x + (topdelta * width) + (y * width)] = 255
        return map, mask

    def save_graymap(self, filename):
        """Save a simple Netpbm file based on picture data.

        The picture format is stored in pixels with values between 0
        and 255. Without colorizing it this is perfect for the Netpbm
        Portable GrayMap image format.
        """
        map, mask = self.get_raster()
        with open(filename, 'wb') as file:
            file.write(b"P5 ")
            file.write(bytes(str(self.width) + " ", 'utf_8'))
            file.write(bytes(str(self.height) + " ", 'utf_8'))
            file.write(b"255 ")
            file.write(map)

    def save_pixmap(self, palette, filename):
        map, mask = self.get_raster()
        with open(filename, 'wb') as file:
            file.write(b"P6 ")
            file.write(bytes(str(self.width) + " ", 'utf_8'))
            file.write(bytes(str(self.height) + " ", 'utf_8'))
            file.write(b"255 ")
            for x, y in zip(map, mask):
                if y == 0:
                    file.write(b'\xff\x00\xff')
                else:
                    color = bytearray.fromhex(palette[x])
                    file.write(color)


class Playpal():
    """A collection of 256-color palettes."""

    def __init__(self, data):
        # TODO: ability to self-generate a palette on command instead
        map0 = []
        for x in range(0, 768, 3):
            map0.append(data[x: x + 3].hex())
        self.maps = [map0,]

    def get_translate(self, word):
        """Change greens to a classic GIBR multiplayer variant."""
        trans = 0
        if word == 'indigo':
            trans = -16
        elif word == 'brown':
            trans = -48
        elif word == 'red':
            trans = -80
        transmap = self.maps[0]
        for x in range(112, 127):
            transmap[x] = transmap[x + trans]
        return transmap


class Post():
    """A short sequence of pixel data."""

    def __init__(self, bytemap):
        # TODO: safety check for 'length' of data
        self.topdelta = read_uint(bytemap[0: 1])
        if self.topdelta < 255:
            length = read_uint(bytemap[1: 2])
            self.unused1 = read_uint(bytemap[2: 3])
            self.data = read_uint_array(bytemap[3: 3 + length], 1)
            self.unused2 = read_uint(bytemap[3 + length: 4 + length])
            self.valid = True
            self.length = length
        else:
            self.valid = False


class Level():
    """Standard Doom level data.

    Doom levels consist of a uniquely-named 'Header' followed by ten
    essential lumps in the following order.

    THINGS
    LINEDEFS
    SIDEDEFS
    VERTEXES
    SEGS
    SSECTORS
    NODES
    SECTORS
    REJECT
    BLOCKMAP
    """

    def __init__(self, **lumps):
        if 'Header' in lumps:
            self.header = lumps['Header']
        if 'THINGS' in lumps:
            data = lumps['THINGS']
            self.things = []
            for x in range(0, len(data), 10):
                thing = Thing(data[x: x + 10])
                self.things.append(thing)
        if 'LINEDEFS' in lumps:
            data = lumps['LINEDEFS']
            self.linedefs = []
            for x in range(0, len(data), 14):
                linedef = Linedef(data[x: x + 14])
                self.linedefs.append(linedef)
        if 'SIDEDEFS' in lumps:
            data = lumps['SIDEDEFS']
            self.sidedefs = []
            for x in range(0, len(data), 30):
                sidedef = Sidedef(data[x: x + 30])
                self.sidedefs.append(sidedef)
        if 'VERTEXES' in lumps:
            vertex_data = lumps['VERTEXES']
            self.vertexes = []
            for x in range(0, len(vertex_data), 4):
                vertex = Vertex(vertex_data[x: x + 4])
                self.vertexes.append(vertex)


class Vertex():
    def __init__(self, data):
        self.x = read_int(data[0: 2])
        self.y = read_int(data[2: 4])


class Thing():
    def __init__(self, data):
        self.x = read_int(data[0: 2])
        self.y = read_int(data[2: 4])
        self.angle = read_int(data[4: 6])
        self.type = read_int(data[6: 8])
        self.flags = read_int(data[8: 10])


class Linedef():
    def __init__(self, data):
        self.start = read_uint(data[0: 2])
        self.end = read_uint(data[2: 4])
        self.flags = read_uint(data[4: 6])
        self.type = read_uint(data[6: 8])
        self.tag = read_uint(data[8: 10])
        self.front = read_uint(data[10: 12])
        self.back = read_uint(data[12: 14])


class Sidedef():
    def __init__(self, data):
        self.xoffs = read_int(bytemap[0: 2])
        self.yoffs = read_int(bytemap[2: 4])
        self.upper = read_str(bytemap[4: 12])
        self.lower = read_str(bytemap[12: 20])
        self.middle = read_str(bytemap[20: 28])
        self.sector = read_int(bytemap[28: 30])


if __name__ == "__main__":
    print(__doc__)
