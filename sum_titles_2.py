#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 从GGB素材的标题中提取所有几何名词

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

stops = [s.strip() for s in open('data/stopwords.txt').readlines()]
titles = json.load(file('data/titles.json'))
print('%d titles' % len(titles))

nltk.download('stopwords')
nltk.download('punkt')
tokens = nltk.tokenize.word_tokenize('\n'.join(titles))
text = nltk.text.Text(tokens)
text.collocations(num=100)

tokens = itertools.imap(lambda t: set(re.split(r'\s', re.sub(r'[^a-z]', ' ', t))), titles)
tokens = list(itertools.chain(*tokens))
tokens = list(itertools.ifilter(lambda t: len(t) > 2 and t not in stops, tokens))
print('%d tokens' % len(set(tokens)))

nltk.download('averaged_perceptron_tagger')
tagged = nltk.pos_tag(tokens)
open('data/_tagged.txt', 'w').write('\n'.join([word + '\t' + tag for word, tag in tagged]))

np = [word for word, tag in tagged if tag in ['NN']]
ns = [word for word, tag in tagged if tag in ['NNS']]
print('NN: %d, NNS: %d' % (len(np), len(ns)))
open('data/_nnp.txt', 'w').write('\n'.join(np))
open('data/_nnps.txt', 'w').write('\n'.join(ns))

# NLTK默认的词性标注对几何错误率高，例如 rectangle 和 bisector 识别为VBP（动词非第三人称单数）
