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
"""Interpret lumps of Doom picture format.
"""

# graymap for rendering images
default_map = bytearray()
for x in range(256):
    default_map.append(x)
    default_map.append(x)
    default_map.append(x)

def ascii_str(data):
    """Tranlate an ascii-encoded byte sequence to string.

    Some Doom strings are padded with null bytes, which are ignored.
    """
    return data.decode('ascii').strip("\0")

def signed_int(data):
    """Translate an signed byte sequence to number."""
    return int.from_bytes(data, byteorder='little', signed=True)

def unsigned_int(data):
    """Translate an unsigned byte sequence to number."""
    return int.from_bytes(data, byteorder='little', signed=False)

def unsigned_int_array(data, size):
    array = []
    for x in range(0, len(data), size):
        value = int.from_bytes(data[x: x + size], byteorder='little',
                signed=False)
        array.append(value)
    return array

class Picture():
    """An image in the Doom picture format.

    This class may be given invalid or corrupted picture data which
    could result in an abnormally long 'columnofs' array or an
    infinitely looping 'posts' extraction, so safeguards are needed to
    prevent either outcome.
    """

    def __init__(self, fd, seek=0):
        try:  # fd is either an open file or a path
            file = open(fd, 'rb')
        except TypeError:
            file = fd
        file.seek(0)
        self.width = unsigned_int(file.read(2))
        self.height = unsigned_int(file.read(2))
        self.leftoffset = signed_int(file.read(2))
        self.topoffset = signed_int(file.read(2))
        safe_width = self.width % 256
        length = 4 * safe_width
        self.columnofs = unsigned_int_array(file.read(length), 4)
        self.columns = []
        if self.width > 255:  # if greater than 256, likely invalid
            return None
        for i, offset in enumerate(self.columnofs):
            file.seek(offset)
            posts, post = [], Post(file)
            while post.valid:
                posts.append(post)
                post = Post(file)
            self.columns.append(posts)
        file.close()
        self.map, self.mask = self.rasterize()

    def rasterize(self):
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

    def save_image(self, filename, playpal=default_map):
        """Save a simple Netpbm file based on picture data.

        The picture format is stored in pixels with values between 0
        and 255.
        """
        width, height = self.width, self.height
        map = [b'\xff\x00\xff' for x in range(width * height)]
        for x, column in enumerate(self.columns):
            for post in column:
                topdelta = post.topdelta
                for y, value in enumerate(post.data):
                    offset = value * 3
                    color = playpal[offset: offset + 3]
                    map[x + (topdelta * width) + (y * width)] = color
        with open(filename, 'wb') as file:
            file.write(b"P6 ")
            file.write(bytes(str(width) + " ", 'utf_8'))
            file.write(bytes(str(height) + " ", 'utf_8'))
            file.write(b"255 ")
            for x in map:
                file.write(x)


class Post():
    """A short sequence of pixel data."""

    def __init__(self, file):
        # TODO: safety check for 'length' of data
        self.topdelta = unsigned_int(file.read(1))
        if self.topdelta < 255:
            length = unsigned_int(file.read(1))
            self.unused1 = unsigned_int(file.read(1))
            self.data = unsigned_int_array(file.read(length), 1)
            self.unused2 = unsigned_int(file.read(1))
            self.valid = True
            self.length = length
        else:
            self.valid = False
