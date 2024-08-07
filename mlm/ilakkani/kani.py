from tqdm import tqdm

from Levenshtein import distance as levenshtein_distance
from tqdm import tqdm

from collections import deque
from pprint import pprint, pformat

import arichuvadi as ari

from ilakkani.valam import DEFAULT_DICTIONARY_FILES
from ilakkani.bloom import build_bloom
from ilakkani.trie import build_trie
from ilakkani.bktree import build_bktree

import json
import string

import ilakkani.valam as valam
import tokenizer

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
            if not thundu.word:
                # spaces are preserved
                continue

            if len(thundu.word) == 1 and thundu.word in string.punctuation:
                continue

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

    def thiruthu(self, ulleedu, veliyeedu):
        for vari in ulleedu:
            #print(vari)
            #thundugal = super().thiruthu(vari.split())
            thundugal = super().thiruthu(
                tokenizer.punct_tokenizer(vari)
            )
            sarivari = ''
            for thundu in thundugal:
                if thundu.correct:
                    sarivari += ' ' + thundu.word
                elif thundu.suggestions:
                    sarivari += ' ' + thundu.word \
                        + '/' \
                        + '/'.join([i[1] for i in thundu.suggestions])
            #print('  ' + sarivari)
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
            'இருக்கு' if trie.prefix_exists_p(ari.get_letters_coding(word)) else 'இல்லை'))

        pprint('என்ன என்ன வார்த்தைகளோ?')
        pprint(bktree.search(word, 2))

        word = input('> ')

    return

import sys
import argparse

def vaayil():
    parser = argparse.ArgumentParser('kani')
    parser.add_argument('input',
                        default=sys.stdin,
                        type=argparse.FileType('r'),
                        help='input file')

    parser.add_argument('output',
                        default=sys.stdout,
                        type=argparse.FileType('w'),
                        help='output file')

    args = parser.parse_args()

    thiruthi = KoappuThiruthi(DEFAULT_DICTIONARY_FILES, suggestions_count=2)
    thiruthi.thiruthu(args.input, args.output)


if __name__ == '__main__':

    vaayil()
    """
    parser = argparse.ArgumentParser('thiruthi')
    parser.add_argument('input',
                        default=sys.stdin,
                        type=argparse.FileType('r'),
                        help='input file')

    parser.add_argument('output',
                        default=sys.stdout,
                        type=argparse.FileType('w'),
                        help='output file')

    args = parser.parse_args()

    thiruthi = KoappuThiruthi(DEFAULT_DICTIONARY_FILES, suggestions_count=2)
    thiruthi.thiruthu(args.input, args.output)

    json_thiruthi = JsonThiruthi([])
    json_thiruthi.copy_dicts(thiruthi)


    #thirutham = json_thiruthi.thiruthu(json.load(open('tharavu/test.json')))
    #pprint(thirutham)

    #main_loop()
    """
