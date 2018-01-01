#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 从GGB素材的标题中提取英文单词及其频次

import sys
import re
import json
import nltk
import itertools
from operator import *

try:
    reload(sys)
    sys.setdefaultencoding('utf-8')
except NameError:
    pass

# 加载停用词和所有标题
stops = [s.strip() for s in open('data/stopwords.txt').readlines()]
titles = json.load(file('data/titles.json'))
print('%d titles' % len(titles))

# 从标题拆分出单词，去掉数字、标点符号等非英文字符，一个标题内的重复单词只计一次
tokens = itertools.imap(lambda t: set(re.split(r'\s', re.sub(r'[^a-z]', ' ', t))), titles)
tokens = list(itertools.chain(*tokens))
# 太短单词和停用词移除
tokens = list(itertools.ifilter(lambda t: len(t) > 2 and t not in stops, tokens))
print('%d tokens' % len(tokens))

# 计算单词的分布频率并保存
freq = nltk.FreqDist(tokens)
lines = ['%s\t%d\n' % (k, v) for k, v in sorted(freq.items(), key=itemgetter(1), reverse=True)]
open('data/_titles.txt', 'w').writelines(lines)

# 绘制前N个单词的分布频率折线图（需要安装matplotlib库）
freq.plot(80)
