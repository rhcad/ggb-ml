#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 基于清华THULAC中文词法分析工具和“结巴”中文分词包试验几题文本解析效果

import sys
import re
import thulac
from jieba import analyse

try:
    reload(sys)
    sys.setdefaultencoding('utf-8')
except NameError:
    pass

sentence = '在△ABC中，AB=AC，△ABC的外接圆⊙O的弦AD的延长线交BC的延长线于点E．求证：△ABD~△AEB．'

tags = '''n/名词 np/人名 ns/地名 ni/机构名 nz/其它专名
m/数词 q/量词 mq/数量词 t/时间词 f/方位词 s/处所词
v/动词 a/形容词 d/副词 h/前接成分 k/后接成分 i/习语
j/简称 r/代词 c/连词 p/介词 u/助词 y/语气助词
e/叹词 o/拟声词 g/语素 w/标点 x/其它'''
tags = {t.split('/')[0]: t.split('/')[1] for t in re.split(r'\s|\n', tags)}

thu1 = thulac.thulac()
c = thu1.cut(sentence)
c = [text + '/' + tag + tags.get(tag, '') for text, tag in c]
print('  '.join(c))

# 在/p介词  △/v动词  ABC/x其它  中/f方位词  ，/w标点  AB/x其它  =/w标点  AC/x其它  ，/w标点  △/v动词
# ABC/x其它  的/u助词  外接/v动词  圆⊙O/ns地名  的/u助词  弦AD/x其它  的/u助词  延长线/nz其它专名
# 交BC/x其它  的/u助词  延长线/nz其它专名  于/p介词  点E．/m数词
# 求证/v动词  ：/w标点  △/v动词  ABD/x其它  ~/w标点  △AEB．/x其它

# c = jieba.cut(sentence, cut_all=True)  # True完全模式，False精确模式(本例句解析失败)
c = analyse.extract_tags(sentence)  # https://my.oschina.net/kakablue/blog/314513
print('  '.join(c))
# ABC  延长线  外接圆  AC  ABD  AD  BC  于点  AB  AEB  求证
