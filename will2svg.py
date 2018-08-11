#!/usr/bin/env python3

import os
import sys
import tempfile
from will2yaml import will2yaml
from yaml2svg import yaml2svg

if len(sys.argv) < 2:
    print("{0} infile.will".format(sys.argv[0]))
    exit()
elif len(sys.argv) == 2:
    temp = tempfile.NamedTemporaryFile(mode = 'w', delete = False)
    temp.write(will2yaml(will_filename = sys.argv[1]))
    temp.close()
    print(yaml2svg(yaml_filename = temp.name))
    os.unlink(temp.name)

