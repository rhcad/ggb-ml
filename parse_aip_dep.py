#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import re

try:
    reload(sys)
    sys.setdefaultencoding('utf-8')
except NameError:
    pass

lines = [(re.sub(r'^\d+\.\s*[^A-Z]+|(（|\().+$|\n', '', t),
          re.sub(r'^\d+\.\s*|[A-Z].+$|\n', '', t))
         for t in open('data/aip_dep_raw.txt').readlines()
         if re.search(ur'^\d+\.\s*[\u4e00-\u9fa5]+[A-Z]+', t.decode('utf-8'))]
open('data/aip_dep.txt', 'w').write('\n'.join(['%s\t%s' % t for t in lines]))
print(len(lines))
