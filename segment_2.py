#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 基于百度自然语言处理服务试验几题文本解析效果

import sys
import re
from aip import AipNlp

try:
    reload(sys)
    sys.setdefaultencoding('utf-8')
except NameError:
    pass

sentence = '在△ABC中，AB=AC，△ABC的外接圆⊙O的弦AD的延长线交BC的延长线于点E．求证：△ABD~△AEB．'

tags = '''n/名词 nr/人名 ns/地名 nt/机构名 nz/其他专名
m/数词 q/量词 t/时间词 f/方位词 s/处所词 nw/作品名
v/动词 vd/动副词 vn/名动词 a/形容词 ad/副形词 an/名形词 d/副词
r/代词 c/连词 p/介词 u/助词 xc/其他虚词 w/标点'''
tags = {t.split('/')[0]: t.split('/')[1] for t in re.split(r'\s|\n', tags)}

APP_ID, API_KEY, SECRET_KEY = open('data/_aip_key.txt').read().split('\n')
client = AipNlp(APP_ID, API_KEY, SECRET_KEY)

res = client.lexer(sentence)    # 词法分析
items = res.get('items', [])
c = [t['item'] + '/' + t['pos'] + tags.get(t['pos'], '') for t in items]
print('  '.join(c))

# 在/p介词  △/w标点  ABC/nz其他专名  中/f方位词  ，/w标点  AB/xc其他虚词  =/xc其他虚词  AC/xc其他虚词
# ，/w标点  △/w标点  ABC/nz其他专名  的/u助词  外接圆/nz其他专名  ⊙/w标点  O/nz其他专名  的/u助词
# 弦/n名词  AD/n名词  的/u助词  延长线/n名词  交/v动词  BC/n名词  的/u助词  延长线/n名词  于/p介词
# 点/n名词  E/xc其他虚词  ．/w标点  求证/vn名动词  ：/w标点  △/w标点  ABD/nz其他专名  ~/w标点
# △/w标点  AEB/nz其他专名  ．/w标点
