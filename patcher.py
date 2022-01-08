#!/usr/bin/env python3
import sys

def main():
    filename = sys.argv[-1]
    header = get_header(filename)

def get_header(filename):
    with open(filename, 'rb') as file:
        width = int.from_bytes(file.read(2), byteorder='little')%256
        height = int.from_bytes(file.read(2), byteorder='little')
        leftoffset = int.from_bytes(file.read(2), byteorder='little')
        topoffset = int.from_bytes(file.read(2), byteorder='little')
        columnofs = int.from_bytes(file.read(4 * width), byteorder='little')
    print(width)
    print(height)
    print(leftoffset)
    print(topoffset)
    print(columnofs)

if __name__ == "__main__":
    try: main()
    except KeyboardInterrupt: print("Keyboard Interrupt (Control-C)...")
    sys.exit()
