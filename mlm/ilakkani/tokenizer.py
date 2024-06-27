import re
from string import punctuation


def whitespace_tokenizer(text):
    return text.split()

def punct_tokenizer(text):
    #r = re.compile(r'[\s{}]+'.format(re.escape(punctuation)))
    r = re.compile(r'(?=[ {0}]+)|(?=[ {0}]+)'.format(re.escape(punctuation)))
    return r.split(text)
