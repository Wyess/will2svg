# Wacom Bamboo Slateの記録データからペン先の軌跡を抽出するPythonスクリプトの作成

## はじめに
WacomのBamboo Slateは「紙に書いたメモやアイデアを、ボタンを押すだけでスマートフォンやタブレットに保存できるスマートパッド」[^1]である。保存したデータはInkscapeというアプリケーションを使用することでPNGやJPEG, PDF, SVG形式でエクスポートすることができる。しかしながら、エクスポートした SVGファイルには太さのある線の輪郭のみが記録されており、中央線（ペン先の軌跡）そのものは記録されていない。この仕様は、エクスポートしたデータをドローソフトで加工する場合に都合が悪い。なぜならば、線の太さや終端形状を容易に変更できないからである。エクスポートできる形式には、ほかにWILL (Wacom Ink Layer Language)と呼ばれるものがある。公開されているWILLの仕様によれば[^2]、筆記データはPath + Stroke Widthsの形式で保存されている。つまり線の輪郭ではなく中央線を抽出することができると考えられ、それを元にペン先の軌跡そのものをpathで表現したSVGファイルも作成できると期待できる。今回はPython 3を用いて検討および実装を行い、それが可能であることを確認した。

## 本文

### WILLファイルの実体はZIPファイル
WILLファイルはZIPファイルであり[^3]、拡張子を.zipに変更すれば中身を見ることができる。パスのデータは/sections/media/paths.protobufに格納されているので、データを抜き出すにはこのファイル形式について知る必要がある。

### Protocol buffer
拡張子が.protobufのファイルはGoogleのProtocol Buffersと呼ばれる形式のファイルで、構造化データをシリアライズするのに用いられる。特定の言語やプラットフォームに依存せず、拡張性が高いとされている[^4] 。データ構造はスキーマを見れば定義が分かるので、WILLのパスのデータ構造を解釈しようと思えば、それに対応するスキーマの情報が必要となる。

### paths.protobufのスキーマ
WILL Data Format Specification[^5]にはパスデータのスキーマが掲載されているが、これを元にデータをパースすると、解釈のできないデータが含まれていることに気づく。完全なスキーマはink SDKのサイト[^6]に掲載されており、これを参照すればpaths.protobufを解釈するのに十分な情報が手に入る。

### 中間形式としてYAMLを使用
*.protobufをデコードするためのコードはスキーマがあれば生成することができるが、Protocol Bufferの仕様を理解するために最小限のコードを自分で書くこととした。デバッグの過程でコンソールに文字列をあれこれ出力していたので、少々の変更を加えてYAML形式で中間ファイルを生成し、それ以降はYAMLをパースする仕様とした。例として以下に中間ファイルの一部を示す。中間ファイルには線の太さや色等の情報も含まれるが、パス抽出後にドローソフトで加工することを前提としているので今回は処理に使用していない。


```yaml
---
startParameter: 0.0
endParameter: 1.0
decimalPrecision: 2
data:
  - [88.68,86.4]
  - [88.68,86.4]
  - [89.04,86.12]
  - [88.68,86.32]
  - [88.84,86.8]
  - [89.08,87.44]
  - [89.36,88.04]
  - [89.68,89.04]
  - [90.2,90.52]
  - [90.76,92.32]
  - [91.36,94.4]
  - [92.0,96.56]
  - [92.68,98.76]
  - [93.36,100.88]
  - [94.04,103.04]
  - [94.76,105.16]
  - [95.44,107.2]
  - [96.12,109.16]
  - [96.76,111.0]
  - [97.32,112.64]
  - [97.72,114.16]
  - [98.16,115.56]
  - [98.52,116.84]
  - [98.76,117.96]
  - [99.0,118.84]
  - [99.12,119.6]
  - [99.2,120.08]
  - [99.24,120.68]
  - [99.4,121.04]
  - [99.2,120.64]
  - [99.08,120.28]
  - [99.0,119.88]
  - [98.96,119.44]
  - [98.84,119.04]
  - [98.72,118.6]
  - [98.6,118.16]
  - [98.36,117.48]
  - [98.16,117.0]
  - [97.96,116.28]
  - [97.68,115.4]
  - [97.36,114.48]
  - [97.08,113.52]
  - [96.76,112.6]
  - [96.44,111.68]
  - [96.12,110.64]
  - [95.72,109.52]
  - [95.32,108.32]
  - [94.96,107.08]
  - [94.56,105.84]
  - [94.24,104.64]
  - [93.88,103.44]
  - [93.56,102.2]
  - [93.2,100.88]
  - [92.84,99.52]
  - [92.52,98.2]
  - [92.24,97.08]
  - [92.04,96.2]
  - [91.88,95.4]
  - [91.76,94.6]
  - [91.64,93.84]
  - [91.56,93.0]
  - [91.48,92.24]
  - [91.48,91.56]
  - [91.48,90.84]
  - [91.48,90.12]
  - [91.52,89.36]
  - [91.48,88.68]
  - [91.52,88.08]
  - [91.48,87.68]
  - [91.48,87.2]
  - [91.36,86.8]
  - [91.2,86.4]
  - [91.0,86.0]
  - [90.68,85.64]
  - [90.28,85.44]
  - [90.16,85.04]
  - [89.92,84.68]
  - [89.84,84.2]
  - [89.84,84.64]
  - [90.16,85.64]
  - [90.36,86.6]
  - [90.72,88.0]
  - [91.08,89.84]
  - [91.48,91.96]
  - [91.88,94.44]
  - [92.2,97.08]
  - [92.68,99.52]
  - [93.2,101.84]
  - [93.8,103.96]
  - [94.4,105.92]
  - [95.04,107.84]
  - [95.56,109.64]
  - [96.12,111.24]
  - [96.68,112.8]
  - [97.16,114.2]
  - [97.68,115.56]
  - [98.2,116.8]
  - [98.48,117.84]
  - [98.8,118.68]
  - [98.96,119.36]
  - [99.12,119.84]
  - [99.28,120.2]
  - [99.52,120.68]
  - [99.96,120.92]
  - [100.28,120.52]
  - [100.48,119.8]
  - [100.64,119.16]
  - [100.8,118.24]
  - [101.08,116.84]
  - [101.36,115.08]
  - [101.72,112.96]
  - [102.08,110.68]
  - [102.44,108.52]
  - [102.84,106.56]
  - [103.16,104.96]
  - [103.48,103.68]
  - [103.76,102.48]
  - [104.04,101.4]
  - [104.32,100.44]
  - [104.56,99.52]
  - [104.8,98.96]
  - [104.88,98.48]
  - [105.12,98.96]
  - [105.36,99.6]
  - [105.6,100.0]
  - [105.8,100.56]
  - [106.12,101.16]
  - [106.44,101.96]
  - [106.84,103.0]
  - [107.32,104.24]
  - [107.88,105.64]
  - [108.52,107.08]
  - [109.16,108.68]
  - [109.84,110.2]
  - [110.52,111.6]
  - [111.16,112.84]
  - [111.76,113.76]
  - [112.32,114.52]
  - [112.8,115.08]
  - [113.28,115.56]
  - [113.72,116.16]
  - [114.16,116.64]
  - [114.6,117.04]
  - [115.08,117.44]
  - [115.48,117.0]
  - [115.72,116.6]
  - [116.0,116.0]
  - [116.32,114.92]
  - [116.68,113.32]
  - [117.08,111.16]
  - [117.6,108.4]
  - [118.2,105.08]
  - [118.88,101.4]
  - [119.52,97.76]
  - [120.04,94.44]
  - [120.48,91.76]
  - [120.72,89.88]
  - [121.04,88.44]
  - [121.2,87.44]
  - [121.28,86.64]
  - [121.4,86.08]
  - [121.48,85.68]
  - [121.4,86.04]
  - [122.64,85.4]
  - [122.64,85.4]
  - [122.64,85.4]
strokeWidths:
  - 1.24
  - 1.23
  - 1.23
  - 1.57
  - 1.99
  - 1.99
  - 1.99
  - 1.98
  - 1.98
  - 1.98
  - 1.98
  - 1.98
  - 1.98
  - 1.98
  - 1.98
  - 1.98
  - 1.98
  - 1.98
  - 1.99
  - 1.99
  - 1.99
  - 1.99
  - 1.99
  - 1.99
  - 1.99
  - 1.99
  - 1.99
  - 1.99
  - 1.99
  - 1.99
  - 1.99
  - 1.99
  - 1.99
  - 1.99
  - 1.99
  - 1.99
  - 1.99
  - 1.99
  - 1.99
  - 1.99
  - 1.99
  - 1.99
  - 1.99
  - 1.99
  - 1.99
  - 1.99
  - 1.99
  - 1.99
  - 1.99
  - 1.99
  - 1.99
  - 1.99
  - 1.99
  - 1.99
  - 1.99
  - 1.99
  - 1.99
  - 1.99
  - 1.99
  - 1.99
  - 1.99
  - 1.99
  - 1.99
  - 1.99
  - 1.99
  - 1.99
  - 1.99
  - 1.99
  - 1.99
  - 1.99
  - 1.99
  - 1.99
  - 1.99
  - 1.92
  - 1.87
  - 1.74
  - 1.85
  - 1.85
  - 1.86
  - 1.92
  - 1.92
  - 1.93
  - 1.94
  - 1.95
  - 1.95
  - 1.96
  - 1.96
  - 1.96
  - 1.97
  - 1.97
  - 1.98
  - 1.98
  - 1.99
  - 1.99
  - 1.99
  - 1.99
  - 1.99
  - 1.99
  - 1.99
  - 1.99
  - 1.99
  - 1.99
  - 1.99
  - 1.99
  - 1.99
  - 1.99
  - 1.99
  - 1.99
  - 1.99
  - 1.99
  - 1.99
  - 1.99
  - 1.99
  - 1.99
  - 1.99
  - 1.99
  - 1.99
  - 1.99
  - 1.99
  - 1.99
  - 1.99
  - 1.99
  - 1.99
  - 1.99
  - 1.99
  - 1.99
  - 1.99
  - 1.99
  - 1.99
  - 1.99
  - 1.99
  - 1.99
  - 1.99
  - 1.99
  - 1.99
  - 1.99
  - 1.99
  - 1.99
  - 1.99
  - 1.99
  - 1.99
  - 1.99
  - 1.99
  - 1.99
  - 1.99
  - 1.99
  - 1.99
  - 1.99
  - 1.99
  - 1.99
  - 1.99
  - 1.99
  - 1.99
  - 1.99
  - 1.99
  - 1.99
  - 1.99
  - 1.99
  - 1.99
  - 1.99
  - 1.99
  - 1.99
  - 1.99
  - 1.91
  - 1.33
  - 1.02
  - 1.02
strokeColor:
  - 255
  - 253
strokeParticlesRandomSeed:
compositeOperation: SOURCE_OVER

```

### Catmull-Rom splineからBezier曲線への変換
path.protobufではpathがCatmull-Rom曲線で記録されている。[^7] Catmull-Rom曲線は3次Bézier曲線で表すことができるため[^8]変換処理を施すことでWILLに記録されているパスの形状を損なうことなくSVGで扱うことができるようになる。

### SVGファイルへの出力
パスデータが用意できれば以下のようなテンプレートと合わせることでSVGファイルとして出力することができる。

```html
<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" width="864" height="1188">
<!-- Path data is inserted here -->
</svg>
```

### 紙面の大きさの取得
WILLファイルの中の/sections/section.svgにはマルチメディアコンテンツをエンコードしたものが記録されている[^9]。この情報を抜き出すことで、SVGを出力する際に適切なサイズを自動的に決定することができる。以下にsection.svgの例を示す。この例ではheight=1188, width=864ということがわかる。

```html
<svg height="1188" width="864" xmlns="http://www.w3.org/2000/svg" xmlns:r="http://schemas.willfileformat.org/2015/relationships">
	<rect fill="#FFFFFF" height="1188" width="864" x="0" y="0"/>
	<g transform="matrix(1 0 0 1 0 0)">
		<g r:id="rId0" transform="matrix(1 0 0 1 0 0)"/>
	</g>
</svg>
```

### ZIPファイルへのアクセス
Pythonの標準ライブラリのzipfileを使用することで、WILLファイルの拡張子を.zipに変更して解凍しファイル名を調べなくてもよいようにした。

### will2yaml.py
WILLファイルから必要なデータを抜き出しYAML形式で書き出すスクリプトは最終的に以下のようになった。

```python
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
        r = re.compile("sections/media/.+\.protobuf")
        strokes_protobuf = list(filter(r.match, will.namelist()))[0]
        info = will.getinfo(strokes_protobuf)
        with will.open(strokes_protobuf) as protobuf:
            data.fromfile(protobuf, info.file_size)
            return protobuf2yaml(data)

def get_page_size(will_filename):
    w, h = 0, 0
    with ZipFile(will_filename) as will:
        r = re.compile("sections/section.*\.svg")
        section_svg = list(filter(r.match, will.namelist()))[0]
        with will.open(section_svg, 'r') as section:
            rw = re.compile('width="([0-9.]+)"')
            rh = re.compile('height="([0-9.]+)"')
            for line in section:
                mw = rw.search(line.decode('utf-8'))
                mh = rh.search(line.decode('utf-8'))
                if mw:
                    w = mw.group(1)
                if mh:
                    h = mh.group(1)
                if w != 0 and h != 0:
                    break

    return w, h

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("{0} file.will".format(sys.argv[0]))
        exit()
    else:
        print(will2yaml(will_filename = sys.argv[1]), end = '')
```

### yaml2svg.py
YAML形式のデータからSVGを作成するスクリプト。処理の中心はCatmull-Rom曲線をBézier曲線に変換する部分である。

```python
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
    if len(sys.argv) != 4:
        print("{0} infile.yaml".format(sys.argv[0]))
        exit()
    elif len(sys.argv) == 4:
        print(yaml2svg(yaml_filename = sys.argv[1], width = sys.argv[2], height = sys.argv[3]))

```

### will2svg.py
will2yaml.pyとyaml2svg.pyを順に実行することでWILLファイルをSVGに変換して出力するスクリプト。

```python
#!/usr/bin/env python3

import os
import sys
import tempfile
from will2yaml import will2yaml, get_page_size
from yaml2svg import yaml2svg

if len(sys.argv) < 2:
    print("{0} infile.will".format(sys.argv[0]))
    exit()
else:
    temp = tempfile.NamedTemporaryFile(mode = 'w', delete = False)
    temp.write(will2yaml(will_filename = sys.argv[1]))
    temp.close()

    #if len(sys.argv) == 2:
    #    print(yaml2svg(yaml_filename = temp.name))
    #else:
    w, h = get_page_size(sys.argv[1])
    outfile =os.path.splitext(sys.argv[1])[0] + '.svg'
    f = open(outfile, 'w')
    f.write(yaml2svg(yaml_filename = temp.name, width = w, height = h))
    f.close()

    os.unlink(temp.name)
```



## まとめ
WacomのBamboo SlateからエクスポートしたWILLファイルから中央線を抽出し、ペン先の軌跡そのものをpathで表現したSVGファイルを出力する、Pythonスクリプトの作成に成功した。出力したSVGファイルの線の太さや終端形状を容易に変更できることも確認できた。成果物はGitHubから入手できる。[^10]

## 参考サイト
[Bamboo Slate small](https://store.wacom.jp/products/detail.php?product_id=3212)

[WILL Data Format](https://developer-docs.wacom.com/display/DevDocs/WILL+Data+Format)

[WILL Data Format Specification](https://developer-docs.wacom.com/display/DevDocs/Format+Specification)

[ink SDK - Encoding and decoding ink content](https://developer-docs.wacom.com/display/DevDocs/ink+SDK+-+Encoding+and+decoding+ink+content)

[globalCompositeOperation プロパティ](http://www.html5.jp/canvas/ref/property/globalCompositeOperation.html)

[Protocol Buffers](https://developers.google.com/protocol-buffers/)

[Is there one-byte type in protobuf?](https://stackoverflow.com/questions/17780300/is-there-one-byte-type-in-protobuf)

[Work with ZIP archives](https://docs.python.org/3/library/zipfile.html)

[How to check file size in python?](https://stackoverflow.com/questions/2104080/how-to-check-file-size-in-python)

[Centripetal Catmull–Rom spline](https://en.wikipedia.org/wiki/Centripetal_Catmull%E2%80%93Rom_spline)


[点列をCatmull Rom曲線を通してBezier曲線列に変換する](http://soma.hatenablog.jp/entry/2016/06/04/210936)

[YAML Ain't Markup Language (YAML™) 1.0](http://yaml.org/spec/1.0/)

[How to parse a YAML file with multiple documents?](https://stackoverflow.com/questions/42522562/how-to-parse-a-yaml-file-with-multiple-documents)



# 附属資料
## Affinity Designerのフォーラム
情報を集めているとき、Bamboo SlateのユーザがSVGのエクスポートに質問しているのを見つけたため、作成したスクリプトについて情報を提供した。それに対する返信として、Macで実際に動かす際に必要だった手順が詳しく述べられている。

[Wacom Bamboo Slate to Affinity Designer: SVG export issue](https://forum.affinity.serif.com/index.php?/topic/50924-wacom-bamboo-slate-to-affinity-designer-svg-export-issue/)

# 注釈
[^1]: [Wacom Bamboo Slate small](https://store.wacom.jp/products/detail.php?product_id=3212)
[^2]: [WILL Data Format](https://developer-docs.wacom.com/display/DevDocs/WILL+Data+Format)
[^3]: [WILL Data Format Appendix B: Store in File Format](https://developer-docs.wacom.com/display/DevDocs/WILL+Data+Format)
[^4]: [Protocol Buffers](https://developers.google.com/protocol-buffers/)
[^5]: [WILL Data Format Specification](https://developer-docs.wacom.com/display/DevDocs/Format+Specification)
[^6]: [ink SDK - Encoding and decoding ink content](https://developer-docs.wacom.com/display/DevDocs/ink+SDK+-+Encoding+and+decoding+ink+content)
[^7]: [WILL Data Format Path](https://developer-docs.wacom.com/display/DevDocs/WILL+Data+Format)
[^8]: [点列をCatmull Rom曲線を通してBezier曲線列に変換する](http://soma.hatenablog.jp/entry/2016/06/04/210936)
[^9]: [WILL Data Format Appendix B: Store in File Format /sections/section.svg](https://developer-docs.wacom.com/display/DevDocs/WILL+Data+Format)
[^10]: [GitHub will2svg](https://github.com/Wyess/will2svg)
