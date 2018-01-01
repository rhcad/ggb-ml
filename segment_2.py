#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 基于百度自然语言处理服务试验几题文本解析效果

import sys
import re
import json
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
client = AipNlp(APP_ID, API_KEY, SECRET_KEY)  # 使用百度云控制台常量创建，需要联网

# 词法分析
res = client.lexer(sentence)
items = res.get('items', [])
c = [t['item'] + '/' + t['pos'] + tags.get(t['pos'], '') for t in items]
print('  '.join(c))

# 在/p介词  △/w标点  ABC/nz其他专名  中/f方位词  ，/w标点  AB/xc其他虚词  =/xc其他虚词  AC/xc其他虚词
# ，/w标点  △/w标点  ABC/nz其他专名  的/u助词  外接圆/nz其他专名  ⊙/w标点  O/nz其他专名  的/u助词
# 弦/n名词  AD/n名词  的/u助词  延长线/n名词  交/v动词  BC/n名词  的/u助词  延长线/n名词  于/p介词
# 点/n名词  E/xc其他虚词  ．/w标点  求证/vn名动词  ：/w标点  △/w标点  ABD/nz其他专名  ~/w标点
# △/w标点  AEB/nz其他专名  ．/w标点

# 依存句法分析
res = client.depParser(sentence)
for t in res.get('items', []):
    print(json.dumps(t, ensure_ascii=False))

'''
{"postag": "p",  "head": 21, "word": "在", "deprel": "ADV"}
{"postag": "w",  "head": 3,  "word": "△", "deprel": "ATT"}
{"postag": "n",  "head": 4,  "word": "ABC", "deprel": "ATT"}
{"postag": "f",  "head": 1,  "word": "中", "deprel": "POB"}
{"postag": "w",  "head": 1,  "word": "，", "deprel": "WP"}
{"postag": "x",  "head": 8,  "word": "AB", "deprel": "ATT"}
{"postag": "w",  "head": 8,  "word": "=", "deprel": "ATT"}
{"postag": "n",  "head": 21, "word": "AC", "deprel": "SBV"}
{"postag": "w",  "head": 8,  "word": "，", "deprel": "WP"}
{"postag": "w",  "head": 12, "word": "△", "deprel": "DE"}
{"postag": "n",  "head": 10, "word": "ABC", "deprel": "COO"}
{"postag": "u",  "head": 13, "word": "的", "deprel": "DE"}
{"postag": "n",  "head": 8,  "word": "外接圆", "deprel": "COO"}
{"postag": "ng", "head": 13, "word": "⊙", "deprel": "COO"}
{"postag": "x",  "head": 16, "word": "O", "deprel": "DE"}
{"postag": "u",  "head": 17, "word": "的", "deprel": "DE"}
{"postag": "n",  "head": 19, "word": "弦", "deprel": "DE"}
{"postag": "n",  "head": 17, "word": "AD", "deprel": "COO"}
{"postag": "u",  "head": 20, "word": "的", "deprel": "DE"}
{"postag": "n",  "head": 8,  "word": "延长线", "deprel": "COO"}
{"postag": "v",  "head": 0,  "word": "交", "deprel": "HED"}
{"postag": "n",  "head": 23, "word": "BC", "deprel": "DE"}
{"postag": "u",  "head": 24, "word": "的", "deprel": "DE"}
{"postag": "n",  "head": 21, "word": "延长线", "deprel": "VOB"}
{"postag": "p",  "head": 21, "word": "于", "deprel": "CMP"}
{"postag": "ng", "head": 25, "word": "点", "deprel": "POB"}
{"postag": "x",  "head": 26, "word": "E", "deprel": "VOB"}
{"postag": "ng", "head": 26, "word": "．", "deprel": "WP"}
{"postag": "v",  "head": 26, "word": "求证", "deprel": "COO"}
{"postag": "w",  "head": 21, "word": "：", "deprel": "WP"}
{"postag": "w",  "head": 21, "word": "△", "deprel": "IC"}
{"postag": "n",  "head": 31, "word": "ABD", "deprel": "COO"}
{"postag": "w",  "head": 31, "word": "~", "deprel": "WP"}
{"postag": "w",  "head": 31, "word": "△", "deprel": "COO"}
{"postag": "n",  "head": 34, "word": "AEB", "deprel": "COO"}
{"postag": "ng", "head": 31, "word": "．", "deprel": "WP"}
'''
