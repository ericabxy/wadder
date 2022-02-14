import os
import sys

from xwadder import Doom, Wads

def main():
    filename = sys.argv[-1]
    if os.path.isfile(filename):
        wad = Wads.Wad(filename)
        andmask1 = 0x00
        for arg in sys.argv:
            if arg[0:11] == "--andmask1=":
                andmask1 = int(arg[11:], base=16)
            elif arg[0:13] == "--save-lumps=":
                # extract and save a standard set of map lumps
                # starting with "map name" and the following 10 lumps
                name = arg[13:]
                if not os.path.exists(name):
                    os.mkdir(name)
                for entry in wad.find_lumps(name, 11):
                    lump = wad.get_lump(entry)
                    filepath = os.path.join(name, entry['name'])
                    Wads.save_lump(lump, filepath)

if __name__ == "__main__":
    try: main()
    except KeyboardInterrupt: print("Keyboard Interrupt (Control-C)...")
    sys.exit()
