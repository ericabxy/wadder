#!/usr/bin/env python3
import os
import re
import sys

from wadder import Wads

def main():
    filename = sys.argv[-1]
    if os.path.isfile(filename):
        header = Wads.get_header(filename)
        directory = Wads.get_directory(
                filename, header['infotableofs'], header['numlumps'])
        for key in header.keys():
            if "--header-" + key in sys.argv:
                print(header[key])
        for arg in sys.argv:
            if arg == "--maps":
                for i, entry in enumerate(directory):
                    mapre = "MAP\d\d\0\0\0"
                    e_mre = "E\dM\d\0\0\0\0"
                    if re.fullmatch(mapre, entry['name']):
                        if "--indexed" in sys.argv:
                            print(i, end=": ")
                        for key in entry.keys():
                            print(entry[key], end=" ")
                        print()
    if len(sys.argv) < 3:
        for key in header.keys():
            print(key + ":", header[key])

if __name__ == "__main__":
    try: main()
    except KeyboardInterrupt: print("Keyboard Interrupt (Control-C)...")
    sys.exit()
