import os
import sys

from xwadder import Levels

from PIL import Image, ImageDraw

def main():
    filename = sys.argv[-1]
    if os.path.isfile(filename):
        pairs, left, top, right, bottom = Levels.load_vertices(filename)
        width, height = right - left, bottom - top
        for arg in sys.argv:
            if arg[0:13] == "--load-lines=":
                name = arg[13:]
                print(os.path.getsize(name))
                linemap = get_lines(name, pairs)
            elif arg == "--save":
                name = os.path.splitext(filename)[0]
                image.save(name + ".png", 'PNG')
            elif arg[0:11] == "--save-lua=":
                print(arg)
                name = arg[11:]
                with open(name + ".lua", 'w') as file:
                    file.write("Lines{\n")
                    for linetup in linemap:
                        file.write("  {")
                        for x in linetup:
                            file.write(str(x) + ", ")
                        file.write("},\n")
                    file.write("}\n")
            elif arg[0:11] == "--save-png=":
                name = arg[11:]
                image = draw_linemap(
                        linemap, left, top, width, height)
                image.save(name + ".png", 'PNG')
            elif arg[0:8] == "--width=":
                width = int(arg[8:])

def get_lines(filename, vertices, andmask1=0x00):
    linemap = []
    file = open(filename, 'rb')
    while not file.closed:
        sv = file.read(2)
        ev = file.read(2)
        flags = file.read(2)
        type = file.read(2)
        tag = file.read(2)
        front = file.read(2)
        back = file.read(2)
        if sv == b'' or ev == b'':
            file.close()
        else:
            vexa = vertices[int.from_bytes(sv, byteorder='little')]
            vexb = vertices[int.from_bytes(ev, byteorder='little')]
            cline = (vexa[0], vexa[1], vexb[0], vexb[1])
            if not flags[0] & andmask1:
                linemap.append(cline)
    return linemap

def draw_linemap(linemap, ox=0, oy=0, width=1024, height=1024):
    image = Image.new('RGB', (width, height), (0, 0, 0))
    draw = ImageDraw.Draw(image)
    for line in linemap:
        x1, y1, x2, y2 = line[0] - ox, line[1] - oy, line[2] - ox, line[3] - oy
        draw.line((x1, y1, x2, y2), fill=(176, 176, 176))
    return image

if __name__ == "__main__":
    try: main()
    except KeyboardInterrupt: print("Keyboard Interrupt (Control-C)...")
    sys.exit()
