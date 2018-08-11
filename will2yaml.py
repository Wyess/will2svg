#!/usr/bin/env python3

from array import array
import struct
import os
import sys
from zipfile import ZipFile
import re


tags = (
    '-', 
    'startParameter',
    'endParameter',
    'decimalPrecision',
    'data',
    'strokeWidths',
    'strokeColor',
    'strokePaint',
    'strokeParticlesRandomSeed',
    'compositeOperation'
)

wire_types = (
    'Variant',
    '64-bit',
    'Length-delimited',
    'Start group',
    'End group',
    '32-bit'
)

compositeOperations = (
    'CLEAR',
    'COPY',
    'SOURCE_OVER',
    'DESTINATION_OVER',
    'SOURCE_IN',
    'DESTINATION_IN',
    'SOURCE_OUT',
    'DESTINATION_OUT',
    'SOURCE_ATOP',
    'DESTINATION_ATOP',
    'XOR',
    'LIGHTER',
    'DIRECT_MULTIPLY',
    'DIRECT_INVERT_SOURCE_MULTIPLY',
    'DIRECT_DARKEN',
    'DIRECT_LIGHTEN',
    'DIRECT_SUBTRACT',
    'DIRECT_REVERSE_SUBTRACT'
)


def __decode_zigzag(val):
    return (val // 2) if (val & 1 == 0) else (-(val + 1) // 2)


def __load_variant(arr, signed = 0):
    val = 0
    i = 0
    while True:
        val |= (arr[i] & 0x7F) << (i * 7)
        i += 1
        if arr[i - 1] & 0x80 == 0:
            break
    if signed:
        val = __decode_zigzag(val)

    return val, i


def protobuf2yaml(data):
    yaml = ''
    i = 0
    to_separate_document = True
    while True:
        if to_separate_document:
            size, di = __load_variant(data[i:])
            i += di
            yaml += '---\n'
            to_separate_document = False
        else:
            tag = (data[i] & 0x78) >> 3
            if tag < len(tags):
                tag = tags[tag]

                if tag == 'startParameter':
                    startParameter = struct.unpack_from('<f', data, i + 1)[0]
                    yaml += "{0}: {1}\n".format(tag, startParameter)
                    i += 1 + 4
                elif tag == 'endParameter':
                    endParameter = struct.unpack_from('<f', data, i + 1)[0]
                    yaml += "{0}: {1}\n".format(tag, endParameter)
                    i += 1 + 4
                elif tag == 'decimalPrecision':
                    decimalPrecision, di = __load_variant(data[i + 1:])
                    yaml += "{0}: {1}\n".format(tag, decimalPrecision)
                    i += 1 + di
                elif tag == 'data':
                    yaml += 'data: \n'
                    size, di = __load_variant(data[i + 1:])
                    i += 1 + di

                    j = 0
                    x, y = 0, 0
                    while j < size:
                        dx, dj = __load_variant(data[i + j:], signed = 1)
                        j += dj

                        dy, dj = __load_variant(data[i + j:], signed = 1)
                        j += dj

                        if j == 0:
                            x, y = dx, dy
                        else:
                            x, y = x + dx, y + dy

                        yaml += "  - [{0},{1}]\n".format(x / (10 ** decimalPrecision), y / (10 ** decimalPrecision))
                    i += size
                elif tag == 'strokeWidths':
                    yaml += 'strokeWidths: \n'
                    size, di = __load_variant(data[i + 1:])
                    i += 1 + di
                    j = 0
                    width = 0
                    while j < size:
                        dw, di = __load_variant(data[i + j:], signed = 1)
                        width += dw
                        j += dj
                        yaml += "  - {0}\n".format(width / (10 ** decimalPrecision))
                    i += size 
                elif tag == 'strokeColor':
                    yaml += "strokeColor: \n"
                    size, di = __load_variant(data[i + 1:])
                    i += 1 + di
                    j = 0
                    color = 0
                    while j < size:
                        dc, di = __load_variant(data[i + j:], signed = 1)
                        color += dc
                        j += dj
                        yaml += "  - {0}\n".format(color)
                    i += size
                elif tag == 'strokePaint':
                    yaml += 'strokePaint: \n'
                    size, di = __load_variant(data[i + 1:])
                    i += 1 + di
                    i += size
                elif tag == 'strokeParticlesRandomSeed':
                    yaml += 'strokeParticlesRandomSeed: \n'
                    size, di = __load_variant(data[i + 1:])
                    i += 1 + di
                    i += size
                elif tag == 'compositeOperation':
                    op, di = __load_variant(data[i + 1:])
                    yaml += "{0}: {1}\n".format(tag, compositeOperations[op])
                    i += 1 + di
                    to_separate_document = True

        if i >= len(data):
            break

    return yaml




def will2yaml(will_filename):
    data = array('B')
    with ZipFile(will_filename) as will:
        r = re.compile("sections/media/strokes-[0-9]+.protobuf")
        strokes_protobuf = list(filter(r.match, will.namelist()))[0]
        info = will.getinfo(strokes_protobuf)
        with will.open(strokes_protobuf) as protobuf:
            data.fromfile(protobuf, info.file_size)
            return protobuf2yaml(data)

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("{0} file.will".format(sys.argv[0]))
        exit()
    else:
        print(will2yaml(will_filename = sys.argv[1]), end = '')
