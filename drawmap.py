#!/usr/bin/env python3
#drawmap - create a PNG from map lumps
#Copyright 2022 Eric Duhamel
#
#This program is free software: you can redistribute it and/or modify
#it under the terms of the GNU General Public License as published by
#the Free Software Foundation, either version 3 of the License, or
#(at your option) any later version.
#
#This program is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#GNU General Public License for more details.
#
#You should have received a copy of the GNU General Public License
#along with this program.  If not, see <https://www.gnu.org/licenses/>.
import os
import sys

from xwadder import Doom, levels, wads

from PIL import Image, ImageDraw

def main():
    if len(sys.argv) > 2 and os.path.isfile(sys.argv[1]):
        filename = sys.argv[1]
        map_name = sys.argv[2]
        wad = wads.Wad(filename)
        map = levels.Level()
        locate = wad.locate_name(map_name)
        for i in range(locate, locate + 11):
            name, lump = wad.get_entry(i)['name'], wad.get_lump(i)
            map.add_lump(name, lump)
        print("drawmap: map lumps")
        for key in map.lumps.keys():
            print("  ", key)
        if map.lumps['VERTEXES'] and map.lumps['LINEDEFS']:
            print("drawmap: combining line definitions with vertices")
            vertexes = Doom.load_vertexes(map.lumps['VERTEXES'])
            linedefs = Doom.load_linedefs(map.lumps['LINEDEFS'])
            print("drawmap: rendering map")
            image = draw_map(linedefs, vertexes)
            savename = "".join([map_name, ".png"])
            print("drawmap: saving to", savename)
            image.save(savename, 'PNG')
    else:
        print("invoked:", sys.argv[0])
        print("usage:")
        print("  python3 drawmap.py [filename] [map name]")

def draw_map(linedefs, vertexes):
    # determine map dimensions
    left, top, right, bottom = 0, 0, 0, 0
    for vertex in vertexes:
        if vertex['x'] < left: left = vertex['x']
        if vertex['x'] > right: right = vertex['x']
        if vertex['y'] < top: top = vertex['y']
        if vertex['y'] > bottom: bottom = vertex['y']
    width, height = right - left, bottom - top
    # draw the map
    image = Image.new('RGB', (width, height), (0, 0, 0))
    draw = ImageDraw.Draw(image)
    for linedef in linedefs:
        start = vertexes[linedef['start']]
        stend = vertexes[linedef['end']]
        x1, y1 = start['x'] - left, start['y'] - top
        x2, y2 = stend['x'] - left, stend['y'] - top
        draw.line((x1, y1, x2, y2), fill=(176, 176, 176))
    return image

if __name__ == "__main__":
    try: main()
    except KeyboardInterrupt: print("Keyboard Interrupt (Control-C)...")
    sys.exit()
