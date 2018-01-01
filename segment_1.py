#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 基于清华THULAC中文词法分析工具包试验几题文本解析效果

import sys
import re
import thulac

try:
    reload(sys)
    sys.setdefaultencoding('utf-8')
except NameError:
    pass

tags = '''n/名词 np/人名 ns/地名 ni/机构名 nz/其它专名
m/数词 q/量词 mq/数量词 t/时间词 f/方位词 s/处所词
v/动词 a/形容词 d/副词 h/前接成分 k/后接成分 i/习语
j/简称 r/代词 c/连词 p/介词 u/助词 y/语气助词
e/叹词 o/拟声词 g/语素 w/标点 x/其它'''
tags = {t.split('/')[0]: t.split('/')[1] for t in re.split(r'\s|\n', tags)}

thu1 = thulac.thulac()
c = thu1.cut(u'如图，已知正方形ABCD的对角线AC、BD相交于点O，E是AC上一点，连结EB，过点A作AM⊥BE，垂足为M，AM交BD于点F．求证：OE=OF；')
c = [text + '/' + tags.get(tag, tag) for text, tag in c]
print('  '.join(c))
