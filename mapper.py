import os
import sys

from xwadder import Wads

def main():
    filename = sys.argv[-1]
    if os.path.isfile(filename):
        wad = Wads.Wad(filename)
        andmask1 = 0x00
        for arg in sys.argv:
            if arg[0:11] == "--andmask1=":
                andmask1 = int(arg[11:], base=16)
            elif arg[0:11] == "--save-lua=":
                name = arg[11:]
                for entry in wad.find_lumps(name, 11):
                    if entry['name'] == "THINGS\0\0":
                        thing_data = wad.get_lump(entry)
                    elif entry['name'] == "LINEDEFS":
                        linedef_data = wad.get_lump(entry)
                    elif entry['name'] == "SIDEDEFS":
                        sidedef_data = wad.get_lump(entry)
                    elif entry['name'] == "VERTEXES":
                        vertex_data = wad.get_lump(entry)
                vertices, box = read_vertices(vertex_data)
                linedefs = read_linedefs(linedef_data)
                sidedefs = read_sidedefs(sidedef_data)
                linemap = read_lines(linedef_data, vertices, andmask1)
                save_quads(linemap, name + ".quads")
                save_lines(linedefs, vertices, name + ".lines")
                save_polys(linedefs, sidedefs, vertices, name + ".polys")
                thingmap = read_things(thing_data)
                save_pairs(thingmap, name + ".things")
            elif arg[0:13] == "--save-lumps=":
                name = arg[13:]
                if not os.path.exists(name):
                    os.mkdir(name)
                for entry in wad.find_lumps(name, 11):
                    lump = wad.get_lump(entry)
                    filepath = os.path.join(name, entry['name'])
                    Wads.save_lump(lump, filepath)

def readint(bytemap, start, length):
    return int.from_bytes(bytemap[start: start + length], byteorder='little')

def read_linedefs(bytemap):
    linedefs = []
    for i in range(0, len(bytemap), 14):
        linedef = {}
        linedef['start'] = readint(bytemap, i, 2)
        linedef['end'] = int.from_bytes(bytemap[i + 2: i + 4],
                                         byteorder='little')
        linedef['flags'] = bytemap[i + 4: i + 6]
        linedef['type'] = int.from_bytes(bytemap[i + 6: i + 8],
                                          byteorder='little')
        linedef['tag'] = int.from_bytes(bytemap[i + 8: i + 10],
                                         byteorder='little')
        linedef['front'] = int.from_bytes(bytemap[i + 10: i + 12],
                                           byteorder='little')
        linedef['back'] = int.from_bytes(bytemap[i + 12: i + 14],
                                          byteorder='little')
        linedefs.append(linedef)
    return linedefs

def read_lines(bytemap, vertices, andmask1=0):
    linemap, linedicts = [], []
    for i in range(0, len(bytemap), 14):
        linedict = {}
        linedict['start'] = readint(bytemap, i, 2)
        linedict['end'] = int.from_bytes(bytemap[i + 2: i + 4],
                                         byteorder='little')
        linedict['flags'] = bytemap[i + 4: i + 6]
        linedict['type'] = int.from_bytes(bytemap[i + 6: i + 8],
                                          byteorder='little')
        linedict['tag'] = int.from_bytes(bytemap[i + 8: i + 10],
                                         byteorder='little')
        linedict['front'] = int.from_bytes(bytemap[i + 10: i + 12],
                                           byteorder='little')
        linedict['back'] = int.from_bytes(bytemap[i + 12: i + 14],
                                          byteorder='little')
        vexa = vertices[linedict['start']]
        vexb = vertices[linedict['end']]
        cline = (vexa[0], vexa[1], vexb[0], vexb[1])
        if not linedict['flags'][0] & andmask1:
            linemap.append(cline)
            linedicts.append(linedict)
    return linemap

def read_sidedefs(bytemap):
    sidedefs = []
    for i in range(0, len(bytemap), 30):
        sidedef = {}
        sidedef['xoffs'] = int.from_bytes(bytemap[i: i + 2],
                                          byteorder='little', signed=True)
        sidedef['yoffs'] = int.from_bytes(bytemap[i + 2: i + 4],
                                          byteorder='little', signed=True)
        sidedef['upper'] = bytemap[i + 4: i + 12].decode('ascii').strip("\0")
        sidedef['lower'] = bytemap[i + 12: i + 20].decode('ascii').strip("\0")
        sidedef['middle'] = bytemap[i + 20: i + 28].decode('ascii').strip("\0")
        sidedef['sector'] = int.from_bytes(bytemap[i + 28: i + 30],
                                           byteorder='little', signed=True)
        sidedefs.append(sidedef)
    return sidedefs

def read_things(bytemap):
    pairs = []
    left, top, right, bottom = 0, 0, 0, 0
    for i in range(0, len(bytemap), 2):
        x = int.from_bytes(
                bytemap[i: i + 2],
                byteorder='little',
                signed=True)
        y = int.from_bytes(
                bytemap[i + 2: i + 4],
                byteorder='little',
                signed=True)
        angle = bytemap[i + 4: i + 6]
        type = bytemap[i + 6: i + 8]
        flags = bytemap[i + 8: i + 10]
        pairs.append((x, y))
        if x < left: left = x
        if x > right: right = x
        if y < top: top = y
        if y > bottom: bottom = y
    return pairs

def read_vertices(bytemap):
    pairs = []
    left, top, right, bottom = 0, 0, 0, 0
    for i in range(0, len(bytemap), 4):
        bx = bytemap[i:i+2]
        by = bytemap[i+2:i+4]
        x = int.from_bytes(bx, byteorder='little', signed=True)
        y = int.from_bytes(by, byteorder='little', signed=True)
        pairs.append((x, y))
        if x < left: left = x
        if x > right: right = x
        if y < top: top = y
        if y > bottom: bottom = y
    return pairs, (left, top, right, bottom)

def save_lines(linedefs, vertices, name):
    with open(name, 'w') as file:
        file.write("Lines{\n")
        for linedef in linedefs:
            start = vertices[linedef['start']]
            stend = vertices[linedef['end']]
            file.write("  {")
            file.write(str(start[0]) + ", ")
            file.write(str(start[1]) + ", ")
            file.write(str(stend[0]) + ", ")
            file.write(str(stend[1]) + "},\n")
        file.write("}\n")

def save_pairs(pairmap, name):
    with open(name, 'w') as file:
        file.write("Pairs{\n")
        for pair in pairmap:
            file.write("  {")
            file.write(str(pair[0]) + ", ")
            file.write(str(pair[1]) + "},\n")
        file.write("}\n")

def save_polys(linedefs, sidedefs, vertices, name):
    with open(name, 'w') as file:
        for linedef in linedefs:
            start = vertices[linedef['start']]
            stend = vertices[linedef['end']]
            if linedef['front'] < 65535:
                sidedef = sidedefs[linedef['front']]
                file.write("Seg{\n")
                file.write("  key = " + str(sidedef['sector']) + ",\n")
                file.write("  line = {")
                file.write(str(start[0]) + ", ")
                file.write(str(start[1]) + ", ")
                file.write(str(stend[0]) + ", ")
                file.write(str(stend[1]) + "},\n}\n")
            if linedef['back'] < 65535:
                sidedef = sidedefs[linedef['back']]
                file.write("Seg{\n")
                file.write("  key = " + str(sidedef['sector']) + ",\n")
                file.write("  line = {")
                file.write(str(start[0]) + ", ")
                file.write(str(start[1]) + ", ")
                file.write(str(stend[0]) + ", ")
                file.write(str(stend[1]) + "},\n}\n")

def save_quads(quadmap, name):
    with open(name, 'w') as file:
        file.write("Lines{\n")
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
