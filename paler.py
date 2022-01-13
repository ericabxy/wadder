#!/usr/bin/env python3
# Extract individual 256-color palettes from PLAYPAL lumps
# Create palette and PLAYPAL lumps from palette text files
import os
import sys

def main():
    if os.path.isfile(sys.argv[-1]):
        filename = sys.argv[-1]
        print_checks(filename)
        if os.path.getsize(filename)%768 == 0:
            pals = int(os.path.getsize(filename)/768)
            print("paler:", pals, "palette(s) detected")
            with open(filename, 'rb') as file:
                if "--file-lumps" in sys.argv:
                    for p in range(pals):
                        print("paler: saving values to pal" + str(p) + ".lmp")
                        saveas_lump(file, "pal" + str(p) + ".lmp")
                elif "--file-pixmaps" in sys.argv:
                    for p in range(pals):
                        print("paler: saving values to pal" + str(p) + ".ppm")
                        saveas_pixmap(file, "pal" + str(p) + ".ppm")
                elif "--file-hexes" in sys.argv:
                    for p in range(pals):
                        print("paler: saving values to pal" + str(p) + ".txt")
                        saveas_text(file, "pal" + str(p) + ".txt")
    else:
        print("paler: not a file '" + sys.argv[1] + "'")

def print_checks(filename):
    print("paler: filename", filename)
    filesize = os.path.getsize(filename)
    if filesize == 10752:
        print("paler: filesize", filesize, "is likely a PLAYPAL lump")
    elif filesize%768 == 0:
        print("paler: filesize", filesize, "may be an RGB palette lump")
    else:
        print("paler: filesize", filesize)
        print("paler: this is likely not a palette lump")

def saveas_lump(file, name):
    """Save the color information in Netpbm format."""
    with open(name, 'wb') as fout:
        for i in range(256):
            color = file.read(3)
            fout.write(color)

def saveas_pixmap(file, name):
    """Save a palette to a PPM file.

    PPM is a minimal pixmap image format and Paler can save each color
    in the palette as a pixel in the image."""
    with open(name, 'wb') as fout:
        fout.write(b"P6 ")
        fout.write(b"16 16 ")
        fout.write(b"255 ")
        for i in range(256):
            color = file.read(3)
            fout.write(color)

def saveas_text(file, name):
    """Save the color information as hex values."""
    with open(name, 'w') as fout:
        for i in range(256):
            color = file.read(3)
            fout.write(color.hex() + "\n")

if __name__ == "__main__":
    try: main()
    except KeyboardInterrupt: print("Keyboard Interrupt (Control-C)...")
    sys.exit()

