#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 基于百度自然语言处理服务试验几题文本解析效果

import os
import sys
import re
import json
from aip import AipNlp

try:
    reload(sys)
    sys.setdefaultencoding('utf-8')
except NameError:
    pass

sentence = '在△ABC中，AB=AC，△ABC的外接圆⊙O的弦AD的延长线交BC的延长线于点E'

tags = '''n/名 nr/人 ns/地 nt/机 nz/专
m/数 q/量 t/时 f/方 s/处 nw/品
v/动 vd/动副 vn/名动 a/形 ad/副形 an/名形 d/副
r/代 c/连 p/介 u/助 xc/虚 w/标
ng/标点 dg/副语 ag/形语 x/字母'''
tags = {t.split('/')[0]: t.split('/')[1] for t in re.split(r'\s|\n', tags)}

APP_ID, API_KEY, SECRET_KEY = open('data/_aip_key.txt').read().split('\n')
client = AipNlp(APP_ID, API_KEY, SECRET_KEY)  # 使用百度云控制台常量创建，需要联网

# 词法分析
pos_file = 'data/_aip_pos.json'
if not os.path.exists(pos_file):
    items = client.lexer(sentence).get('items', [])
    open(pos_file, 'w').write(json.dumps(items, ensure_ascii=False))
else:
    items = json.load(file(pos_file))
c = [t['item'] + '/' + t['pos'] + tags.get(t['pos'], '') for t in items]
print('  '.join(c))

# 在/p介词  △/w标点  ABC/nz其他专名  中/f方位词  ，/w标点  AB/xc其他虚词  =/xc其他虚词  AC/xc其他虚词  ，/w标点
# △/w标点  ABC/nz其他专名  的/u助词  外接圆/nz其他专名  ⊙/w标点  O/nz其他专名  的/u助词  弦/n名词  AD/n名词  的/u助词
# 延长线/n名词  交/v动词  BC/n名词  的/u助词  延长线/n名词  于/p介词  点/n名词  E/xc其他虚词


# 依存句法分析
def print_dep(pid):
    berkel = ''
    for i, t in enumerate(res):
        if t['head'] == pid:
            postag = tags.get(t['postag'], '')
            deprel = dep.get(t['deprel'], '')
            text = print_dep(i + 1)
            berkel += ' ({0}/{1}{2} {3})'.format(t['word'], postag, deprel, text)
    return berkel


dep = {r.split('\t')[0]: r.split('\t')[1] for r in open('data/aip_dep.txt').read().split('\n')}
dep_file = 'data/_aip_dep.json'
if not os.path.exists(dep_file):
    res = client.depParser(sentence).get('items', [])
    open(dep_file, 'w').write(json.dumps(res, ensure_ascii=False))
else:
    res = json.load(file(dep_file))
print(print_dep(0))
'''
(交/动核心  (在/介状中  (中/方介宾  (ABC/名定中  (△/标定中 ))) (，/标标点 ))
    (AC/名主谓  (AB/字母定中 ) (=/标定中 ) (，/标标点 )
        (外接圆/名并列  (的/助的字  (△/标的字  (ABC/名并列 ))) (⊙/标点并列 ))
        (延长线/名并列  (的/助的字  (弦/名的字  (的/助的字  (O/字母的字 )) (AD/名并列 )))))
    (延长线/名动宾  (的/助的字  (BC/名的字 )))
    (于/介动补  (点/标点介宾  (E/字母附加 ))))

1       	交      /v  动词      	HED 核心
11      	在      /p  介词      	ADV 状中结构
111     	中      /f  方位词     	POB 介宾关系
1111    	ABC    /n  名词      	ATT 定中关系
11111   	△      /w  标点      	ATT 定中关系
112     	，      /w  标点      	WP  标点
12      	AC     /n  名词      	SBV 主谓关系
121     	AB     /x  字母      	ATT 定中关系
122     	=      /w  标点      	ATT 定中关系
123     	，      /w  标点      	WP  标点
124     	外接圆    /n  名词      	COO 并列关系
1241    	的      /u  助词      	DE  的字结构
12411   	△      /w  标点      	DE  的字结构
124111  	ABC    /n  名词      	COO 并列关系
1242    	⊙      /ng 标点      	COO 并列关系
125     	延长线    /n  名词      	COO 并列关系
1251    	的      /u  助词      	DE  的字结构
12511   	弦      /n  名词      	DE  的字结构
125111  	的      /u  助词      	DE  的字结构
1251111 	O      /x  字母      	DE  的字结构
125112  	AD     /n  名词      	COO 并列关系
13      	延长线    /n  名词      	VOB 动宾关系
131     	的      /u  助词      	DE  的字结构
1311    	BC     /n  名词      	DE  的字结构
14      	于      /p  介词      	CMP 动补结构
141     	点      /ng 标点      	POB 介宾关系
1411    	E      /x  字母      	ADJ 附加关系
'''
