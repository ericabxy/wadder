import os
import sys

from wadder import Levels

from PIL import Image, ImageDraw

def main():
    filename = sys.argv[-1]
    if os.path.isfile(filename):
        pairs = Levels.load_vertices(filename)
        ox, oy, width, height = 1024, 1024, 2048, 2048
        for arg in sys.argv:
            if arg[0:13] == "--draw-lines=":
                name = arg[13:]
                image = draw_lines(name, pairs, ox, oy, width, height)
            elif arg[0:9] == "--height=":
                height = int(arg[9:])
            elif arg == "--save":
                name = os.path.splitext(filename)[0]
                image.save(name + str(ox) + "." + str(oy) + ".png", 'PNG')
            elif arg[0:11] == "--origin-x=":
                ox = int(arg[11:])
            elif arg[0:11] == "--origin-y=":
                oy = int(arg[11:])
            elif arg[0:8] == "--width=":
                width = int(arg[8:])

def draw_lines(filename, vertices, ox=0, oy=0, width=1024, height=1024):
    image = Image.new('RGB', (width, height), (0, 0, 0))
    draw = ImageDraw.Draw(image)
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
            one_sided = flags[0] & 0x04
            secret_line = flags[0] & 0x20
            start = vertices[int.from_bytes(sv, byteorder='little')]
            ender = vertices[int.from_bytes(ev, byteorder='little')]
            color = (255, 0, 0)
            color = (176, 176, 176) if one_sided else color
            color = (255, 0, 255) if secret_line else color
            blue = blue if flags[0] & 0x20 else 176
            cline = (start[0] + ox, -start[1] + oy,
                     ender[0] + ox, -ender[1] + oy)
            draw.line(cline, fill=color)
    return image

if __name__ == "__main__":
    try: main()
    except KeyboardInterrupt: print("Keyboard Interrupt (Control-C)...")
    sys.exit()
