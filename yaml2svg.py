#!/usr/bin/env python3

import yaml
import sys

def catmull_rom_to_bezier(data):
    bezier = ''
    x  = [0, 0, 0, 0]
    y  = [0, 0, 0, 0]
    px = [0, 0, 0, 0]
    py = [0, 0, 0, 0]

    bezier += "M {0:.2f} {1:.2f}".format(data[0][0], data[0][1])
    for i in range(1, len(data) - 2):
        x[0], y[0] = data[i - 1]
        x[1], y[1] = data[i]
        x[2], y[2] = data[i + 1]
        x[3], y[3] = data[i + 2]

        px[0], py[0] = x[1], y[1]
        px[1], py[1] = (-x[0] + 6 * x[1] + x[2]) / 6, (-y[0] + 6 * y[1] + y[2]) / 6
        px[2], py[2] = ( x[1] + 6 * x[2] - x[3]) / 6, ( y[1] + 6 * y[2] - y[3]) / 6
        px[3], py[3] = x[2], y[2]
        
        bezier += " C"
        for k in (1, 2, 3):
            bezier += " {0:.2f} {1:.2f}".format(px[k], py[k])
    return bezier

def yaml2svg(yaml_filename, width, height):
    svg = ''
    with open(yaml_filename) as stream:
        svg += '<?xml version="1.0" encoding="UTF-8"?>'
        svg += '<svg xmlns="http://www.w3.org/2000/svg" width="{0}" height="{1}">'.format(width, height)
        #svg += '<rect fill="#FFFFFF" fill-opacity="1.0" width="592.0" height="864.0"/>'
        #svg += '<g transform="matrix(1.0 0.0 0.0 1.0 0.0 0.0)" fill="none" stroke="#000000">'

        docs = yaml.safe_load_all(stream)
        for doc in docs:
            path = catmull_rom_to_bezier(doc['data'])
            svg += '<path fill="none" stroke="#000000" stroke-linecap="round" d="{0}" />'.format(path)

        #svg += '</g>'
        svg += '</svg>'
    return svg

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("{0} infile.yaml".format(sys.argv[0]))
        exit()
    elif len(sys.argv) == 4:
        print(yaml2svg(yaml_filename = sys.argv[1], width = sys.argv[2], height = sys.argv[3]))
