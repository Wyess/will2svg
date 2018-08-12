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
    
