import os
import sys

def main():
    filename = sys.argv[-1]
    if os.path.isfile(filename):
        res = 64
        width, height, origin, intmap = scale(res)
        file = open(filename, 'rb')
        for arg in sys.argv:
            if arg[0:13] == "--resolution=":
                res = int(arg[13:])
                width, height, origin, intmap = scale(res)
        bits, intmap = load_maps(filename, res)
        save_bitmap(bits, width, height, "vertexes")
        save_graymap(intmap, width, height, "vertexes")

def load_maps(filename, res):
    width, height = int(65536 / res), int(65536 / res)
    origin = int(65536 / res / 2)
    bitstring = "1" * width * height
    intmap = [0 for x in range(width * height)]
    file = open(filename, 'rb')
    i = 1
    while not file.closed:
        bx = file.read(2)
        by = file.read(2)
        x = int.from_bytes(bx, byteorder='little', signed=True)
        y = int.from_bytes(by, byteorder='little', signed=True)
        if bx == b'' or by == b'':
            file.close()
        else:
            px, py = int(x / res) + origin, int(y / res) + origin
            pos = (width * height - width) + px - (width * py)
            bitstring = bitstring[0:pos] + "0" + bitstring[pos+1:]
            intmap[pos] = i % 256
        i = i + 1
    return bitstring, intmap

def load_vertices(filename):
    pairs = []
    file = open(filename, 'rb')
    while not file.closed:
        bx = file.read(2)
        by = file.read(2)
        x = int.from_bytes(bx, byteorder='little', signed=True)
        y = int.from_bytes(by, byteorder='little', signed=True)
        if bx == b'' or by == b'':
            file.close()
        else:
            pairs.append((x, y))
    return pairs

def scale(div):
    width, height = int(65536 / div), int(65536 / div)
    origin = int(65536 / div / 2)
    bitmap = [0 for x in range(width * height)]
    return width, height, origin, bitmap

def save_bitmap(bitmap, width, height, name):
    with open(name + ".pbm", 'wb') as file:
        file.write(b"P4 ")
        file.write(bytes(str(width) + " ", 'utf_8'))
        file.write(bytes(str(height) + " ", 'utf_8'))
        bytemap = bytearray()
        for i in range(0, len(bitmap), 8):
            bytemap.append(int(bitmap[i:i+8], 2))
        file.write(bytemap)

def save_graymap(bitmap, width, height, name):
    with open(name + ".pgm", 'wb') as file:
        file.write(b"P5 ")
        file.write(bytes(str(width) + " ", 'utf_8'))
        file.write(bytes(str(height) + " ", 'utf_8'))
        file.write(b"255 ")
        for b in bitmap:
            file.write(b.to_bytes(1, 'little'))

if __name__ == "__main__":
    try: main()
    except KeyboardInterrupt: print("Keyboard Interrupt (Control-C)...")
    sys.exit()
