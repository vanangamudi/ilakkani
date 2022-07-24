from tqdm import tqdm
from bktree import BKTree
from trie import Trie

from Levenshtein import distance as levenshtein_distance
from tqdm import tqdm
from tamil.utf8 import get_letters
from collections import deque
from pprint import pprint, pformat

from resources import DEFAULT_DICTIONARY_FILES
from bloom import build_bloom
from trie import build_trie
from bktree import build_bktree

import json

import resources

class Thundu:
    def __init__(self, word):
        self.word = word
        self.suggestions = []
        self.correct = False

    def __json__(self):
        return {
            'word' : self.word,
            'suggestions' : self.suggestions,
            'correct_p' : self.correct
        }
    

class Thiruthi:
    def __init__(self,
                 filepaths = DEFAULT_DICTIONARY_FILES,
                 suggestions_count = 5):
        self.bloom   = build_bloom(filepaths, 200000, 0.05)
        self.trie    = build_trie(filepaths)
        self.bktree  = build_bktree(filepaths)

        self.suggestions_count = suggestions_count

    def _thiruthu(self, thundugal):

        for thundu in thundugal:
            if thundu.word in self.bloom:
                thundu.correct = True
                continue

            if self.trie.prefix_exists_p(thundu.word):
                thundu.correct = True
                continue

            thundu.suggestions.extend(
                self.bktree.search(thundu.word, 2)[:self.suggestions_count]
            )

        return thundugal

    def thiruthu(self, words):
        thundugal = [Thundu(i) for i in words]
        return self._thiruthu(thundugal)

    def copy_dicts(self, other):
        self.bloom = other.bloom
        self.trie = other.trie
        self.bktree = other.bktree

class KoappuThiruthi(Thiruthi):
    def __init__(self, filepaths, suggestions_count=5):
        super().__init__(filepaths, suggestions_count)

    def thiruthu(self, filepath):
        print('checking {}'.format(filepath))
        ulleedu   = open(filepath)
        veliyeedu = open(filepath + '.thiruthi', 'w')
        
        print('writing to {}'.format(filepath+ '.thiruthi', 'w'))

        for vari in ulleedu:
            print(vari)
            thundugal = super().thiruthu(vari.split())
            sarivari = ''
            for thundu in thundugal:
                if thundu.correct:
                    sarivari += ' ' + thundu.word
                elif thundu.suggestions:
                    sarivari += ' ' + thundu.word \
                        + '/' \
                        + '/'.join([i[1] for i in thundu.suggestions])
            print('  ' + sarivari)
            print(sarivari, file=veliyeedu)
            

class JsonThiruthi(Thiruthi):
    def __init__(self, filepaths, suggestions_count=5):
        super().__init__(filepaths, suggestions_count)

    def thiruthu(self, ulleedu_json):
        thundugal = super().thiruthu(ulleedu_json['chorkal'])
        thirutham = [i.__json__() for i in thundugal]
        ulleedu_json['thirutham'] = thirutham
        return ulleedu_json

bloom = None
trie = None
bktree = None

def main_loop():
    global bloom, trie, bktree
    bloom   = build_bloom(DEFAULT_DICTIONARY_FILES, 200000, 0.05)
    trie    = build_trie(DEFAULT_DICTIONARY_FILES)
    bktree  = build_bktree(DEFAULT_DICTIONARY_FILES)

    word = input('> ')
    while word:
        print('இருக்குதா? {}'.format(
            'இருக்கு' if word in bloom  else 'இல்லை'))
        

        print('இருக்குதா? {}'.format(
            'இருக்கு' if trie.prefix_exists_p(get_letters(word)) else 'இல்லை'))
        
        pprint('என்ன என்ன வார்த்தைகளோ?')
        pprint(bktree.search(word, 2))
        
        word = input('> ')

    return

import sys
import argparse
if __name__ == '__main__':

    parser = argparse.ArgumentParser('thiruthi')
    parser.add_argument('-i', '--input',
                        default=f'{resources.THARAVU_VER}/test.txt',
                        help='input fle')

    parser.add_argument('-o', '--output',
                        default=f'{resources.THARAVU_VER}/test.txt.thiruthi',
                        help='output fle')

    args = parser.parse_args()
        
    thiruthi = KoappuThiruthi(DEFAULT_DICTIONARY_FILES, suggestions_count=2)
    thiruthi.thiruthu(args.input)

    json_thiruthi = JsonThiruthi([])
    json_thiruthi.copy_dicts(thiruthi)

    
    #thirutham = json_thiruthi.thiruthu(json.load(open('tharavu/test.json')))
    #pprint(thirutham)
    
    #main_loop()
