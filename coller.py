#!/usr/bin/env python3
import os
import sys

def main():
    filename = sys.argv[-1]
    if os.path.isfile(filename):
        with open(filename, 'rb') as file:
            colormap = file.read(256)
        for arg in sys.argv:
            if arg[0:7] == "--load=":
                index = int(arg[7:])
                with open(filename, 'rb') as file:
                    file.seek(index * 256)
                    colormap = bytearray(file.read(256))
            elif arg == "--save-lump":
                name = os.path.splitext(filename)[0] + str(index) + ".lmp"
                with open(name, "wb") as file:
                    file.write(colormap)
            elif arg[0:8] == "--start=":
                start = int(arg[8:])
            elif arg[0:8] == "--shift=":
                shift = int(arg[8:])
                colormap[start:stop] = [x + shift for x in colormap[start:stop]]
            elif arg[0:7] == "--stop=":
                stop = int(arg[7:])
    else:
        print("paller: not a file '" + filename + "'")


def check_file(filename):
    print("paller: filename", filename)
    filesize = os.path.getsize(filename)
    if filesize == 10752:
        print("paller: filesize", filesize, "is likely a PLAYPAL lump")
        print("paller:", filesize//768, "palette(s) detected")
    elif filesize%768 == 0:
        print("paller: filesize", filesize, "may be an RGB palette lump")
        print("paller:", filesize//768, "palette(s) detected")
    else:
        print("paller: filesize", filesize)
        print("paller: this is likely not a palette lump")

def load_playpal(filename, index):
    with open(filename, 'rb') as file:
        file.seek(768 * index)
        playpal = file.read(768)
    return playpal

def read_hexmap(filename):
    """Return 256 hex-encoded values read from a file."""
    map = []
    with open(filename) as file:
        for i in range(256):
            map.append(file.readline())
    return map

def save_graymap(bytemap, name):
    """Save bytes to a 4096-pixel Portable GrayMap."""
    with open(name, 'wb') as file:
        file.write(b"P5 ")
        file.write(b"64 64 ")
        file.write(b"255 ")
        file.write(bytemap)

def save_lump(bytemap, name):
    """Save palette as lump data."""
    with open(name, 'wb') as file:
        file.write(bytemap)

def save_pixmap(playpal, name):
    """Save remapped bytes to a Portable PixMap file."""
    with open(name, 'wb') as file:
        file.write(b"P6 ")
        file.write(b"16 16 ")
        file.write(b"255 ")
        for i in range(0, 768, 3):
            color = playpal[i:i+3]
            file.write(color)

def save_hexmap(playpal, name):
    """Save each color value in hexadecimal."""
    with open(name, 'w') as file:
        for i in range(0, 768, 3):
            name = playpal[i:i+3].hex()
            file.write(name + "\n")

if __name__ == "__main__":
    try: main()
    except KeyboardInterrupt: print("Keyboard Interrupt (Control-C)...")
    sys.exit()

