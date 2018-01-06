#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 从GGB素材的标题中提取英文单词及其频次

import sys
import re
import json
import nltk
from nltk.stem import PorterStemmer as Stemmer
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
# tokens = itertools.imap(lambda t: set(re.split(r'\s', re.sub(r'[^a-z]', ' ', t))), titles)
# tokens = list(itertools.chain(*tokens))  # 变为一维数组

# 从标题拆分出单词，移除太短单词、全数字、日俄韩阿拉伯字、停用词
tokens = nltk.tokenize.word_tokenize('\n'.join(titles))
ignores = re.compile(ur'^[0-9.]+$|[\u0800-\u4e00\u0400-\u052f\u3130-\u318F\uAC00-\uD7A3\u0600-\u06FF]')
tokens = list(itertools.ifilter(lambda t: len(t) > 1 and not ignores.search(t) and t not in stops, tokens))

# 多语言同义词
synonym_ = {
    u'recta': 'rectangle',
    u'rectangl': 'rectangle',
    u'triangl': 'triangle',
    u'triángulo': 'triangle',
    u'triangolo': 'triangle',
    u'copi': 'copy',
    u'teorema': 'theorem',
    u'equat': 'equation',
    u'funcion': 'function',
    u'fonction': 'function',
    u'funktion': 'function',
    u'funzion': 'function',
    u'função': 'function',
    u'problema': 'problem',
    u'rotati': 'rotate',
    u'cercl': 'circle',
    u'circunferencia': 'circumferentia',
    u'angl': 'angle',
    u'ángulo': 'angle',
    u'sin': 'sine',
    u'tarea': 'task',
    u'plano': 'plane',
    u'área': 'area',
    u'punto': 'point',
}

synonym_s = {
    'exerci': 'exercise',
    'invest': 'invest',
    'activ': 'activity'
}


def synonym(word):
    if word in synonym_:
        return synonym_[word]
    for s in synonym_s:
        if word.startswith(s):
            return synonym_s[s]
    return word


# 词干提取
st = Stemmer()
ignores = re.compile(r'^[-_*/]+|[-_]$|\.ggb$|[.-_]?\d+[.-_]?|')
tokens = list(itertools.ifilter(lambda t: len(t) > 2, itertools.imap(
    lambda t: synonym(st.stem(ignores.sub('', t))), tokens)))
print('%d tokens' % len(set(tokens)))

# 计算单词的频率分布并保存
freq = nltk.FreqDist(tokens)
items = [t for t in freq.items() if t[1] > 10]
lines = ['%s\t%d\n' % (k, v) for k, v in sorted(items, key=itemgetter(1), reverse=True)]
open('data/_titles.txt', 'w').writelines(lines)

# 绘制前N个单词的频率分布折线图（需要安装matplotlib库）
freq.plot(80)
