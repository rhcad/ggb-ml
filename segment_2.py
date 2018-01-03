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
r/代词 c/连词 p/介词 u/助词 xc/其他虚词 w/标点
ng/标点 dg/副语素 ag/形语素 x/字母'''
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
dep = {r.split('\t')[0]: r.split('\t')[1] for r in open('data/aip_dep.txt').read().split('\n')}
res = client.depParser(sentence)  # 返回值没有id？
for i, t in enumerate(res.get('items', [])):
    print('id: %-2d\thead: %-2d\tword: %-6s\tpostag: %-2s %-8s\tdeprel: %-3s %s' %
          (t.get('id', i), t['head'], t['word'], t['postag'], tags.get(t['postag'], ''),
           t['deprel'], dep.get(t['deprel'], '')))

'''
id: 0 	head: 21	word: 在     	postag: p  介词      	deprel: ADV 状中结构
id: 1 	head: 3 	word: △     	postag: w  标点      	deprel: ATT 定中关系
id: 2 	head: 4 	word: ABC   	postag: n  名词      	deprel: ATT 定中关系
id: 3 	head: 1 	word: 中     	postag: f  方位词     	deprel: POB 介宾关系
id: 4 	head: 1 	word: ，     	postag: w  标点      	deprel: WP  标点
id: 5 	head: 8 	word: AB    	postag: x  字母      	deprel: ATT 定中关系
id: 6 	head: 8 	word: =     	postag: w  标点      	deprel: ATT 定中关系
id: 7 	head: 21	word: AC    	postag: n  名词      	deprel: SBV 主谓关系
id: 8 	head: 8 	word: ，     	postag: w  标点      	deprel: WP  标点
id: 9 	head: 12	word: △     	postag: w  标点      	deprel: DE  的字结构
id: 10	head: 10	word: ABC   	postag: n  名词      	deprel: COO 并列关系
id: 11	head: 13	word: 的     	postag: u  助词      	deprel: DE  的字结构
id: 12	head: 8 	word: 外接圆   	postag: n  名词      	deprel: COO 并列关系
id: 13	head: 13	word: ⊙     	postag: ng 标点      	deprel: COO 并列关系
id: 14	head: 16	word: O     	postag: x  字母      	deprel: DE  的字结构
id: 15	head: 17	word: 的     	postag: u  助词      	deprel: DE  的字结构
id: 16	head: 19	word: 弦     	postag: n  名词      	deprel: DE  的字结构
id: 17	head: 17	word: AD    	postag: n  名词      	deprel: COO 并列关系
id: 18	head: 20	word: 的     	postag: u  助词      	deprel: DE  的字结构
id: 19	head: 8 	word: 延长线   	postag: n  名词      	deprel: COO 并列关系
id: 20	head: 0 	word: 交     	postag: v  动词      	deprel: HED 核心
id: 21	head: 23	word: BC    	postag: n  名词      	deprel: DE  的字结构
id: 22	head: 24	word: 的     	postag: u  助词      	deprel: DE  的字结构
id: 23	head: 21	word: 延长线   	postag: n  名词      	deprel: VOB 动宾关系
id: 24	head: 21	word: 于     	postag: p  介词      	deprel: CMP 动补结构
id: 25	head: 25	word: 点     	postag: ng 标点      	deprel: POB 介宾关系
id: 26	head: 26	word: E     	postag: x  字母      	deprel: VOB 动宾关系
id: 27	head: 26	word: ．     	postag: ng 标点      	deprel: WP  标点
id: 28	head: 26	word: 求证    	postag: v  动词      	deprel: COO 并列关系
id: 29	head: 21	word: ：     	postag: w  标点      	deprel: WP  标点
id: 30	head: 21	word: △     	postag: w  标点      	deprel: IC  独立分句
id: 31	head: 31	word: ABD   	postag: n  名词      	deprel: COO 并列关系
id: 32	head: 31	word: ~     	postag: w  标点      	deprel: WP  标点
id: 33	head: 31	word: △     	postag: w  标点      	deprel: COO 并列关系
id: 34	head: 34	word: AEB   	postag: n  名词      	deprel: COO 并列关系
id: 35	head: 31	word: ．     	postag: ng 标点      	deprel: WP  标点
'''
