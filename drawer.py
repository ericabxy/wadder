import os
import sys

from xwadder import Levels, Wads

from PIL import Image, ImageDraw

def main():
    filename = sys.argv[-1]
    if os.path.isfile(filename):
        wad = Wads.Wad(filename)
        andmask1 = 0x00
        for arg in sys.argv:
            if arg[0:11] == "--andmask1=":
                andmask1 = int(arg[11:], base=16)
            elif arg[0:11] == "--save-png=":
                name = arg[11:]
                for entry in wad.find_lumps(name, 11):
                    if entry['name'] == "VERTEXES":
                        vertex_data = wad.get_lump(entry)
                    elif entry['name'] == "LINEDEFS":
                        linedef_data = wad.get_lump(entry)
                assert "vertex_data" in locals(), "no map found"
                vertices, box = Levels.read_vertices(vertex_data)
                linemap = read_lines(linedef_data, vertices, andmask1)
                left, top = box[0], box[1]
                width, height = box[2] - left, box[3] - top
                image = draw_linemap(linemap, left, top, width, height)
                image.save(name + ".png", 'PNG')
        if len(sys.argv) < 3:  # if no command arguments
            wad.report()
    if len(sys.argv) < 2:  # if no filename
        print("drawer: please pass a WAD file as an argument")

def draw_linemap(linemap, ox=0, oy=0, width=1024, height=1024):
    image = Image.new('RGB', (width, height), (0, 0, 0))
    draw = ImageDraw.Draw(image)
    for line in linemap:
        x1, y1 = line[0] - ox, line[1] - oy
        x2, y2 = line[2] - ox, line[3] - oy
        draw.line((x1, y1, x2, y2), fill=(176, 176, 176))
    return image

def read_lines(bytemap, vertices, andmask1=0):
    linemap = []
    for i in range(0, len(bytemap), 14):
        sv = bytemap[i: i + 2]
        ev = bytemap[i + 2: i + 4]
        flags = bytemap[i + 4: i + 6]
        type = bytemap[i + 6: i + 8]
        tag = bytemap[i + 8: i + 10]
        front = bytemap[i + 10: i + 12]
        back = bytemap[i + 12: i + 14]
        vexa = vertices[int.from_bytes(sv, byteorder='little')]
        vexb = vertices[int.from_bytes(ev, byteorder='little')]
        cline = (vexa[0], vexa[1], vexb[0], vexb[1])
        if not flags[0] & andmask1:
            linemap.append(cline)
    return linemap

def save_pairs(pairmap, name):
    with open(name, 'w') as file:
        file.write("Pairs{\n")
        for pair in pairmap:
            file.write("  {")
            file.write(str(pair[0]) + ", ")
            file.write(str(pair[1]) + "},\n")
        file.write("}\n")

def save_quads(quadmap, name):
    with open(name, 'w') as file:
        file.write("Quads{\n")
        for quad in quadmap:
            file.write("  {")
            file.write(str(quad[0]) + ", ")
            file.write(str(quad[1]) + ", ")
            file.write(str(quad[2]) + ", ")
            file.write(str(quad[3]) + "},\n")
        file.write("}\n")

if __name__ == "__main__":
    try: main()
    except KeyboardInterrupt: print("Keyboard Interrupt (Control-C)...")
    sys.exit()
