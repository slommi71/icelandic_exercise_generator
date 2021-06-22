#!/usr/bin/env python
# -*- coding: utf-8 -*-
# pylint: disable=line-too-long,broad-except

""" returns yaml structrure for a word from arnastofnun"""


import requests
import json
from pprint import pprint
from argparse import ArgumentParser


class arnastofnun:

    def __init__(self, word, wordclass):
        self.baseurl = "https://bin.arnastofnun.is/api/ord"
        self.word = word
        self.wordclass = wordclass
        self.ord_dict = {}
        self.translate_abbrev = {
            'kk': 'karlkyns',
            'kvk': 'kvenkyns',
            'hk': 'hvorugkyns',
            'no': 'nafnorð',
            'so': 'sagnorð'
        }
        if wordclass == 'no':
            self.no_beygingarmyndir = {}
        elif wordclass == 'so':
            self.so_beygingarmyndir = {}

        self.url = self.get_url()


    def get_url(self):
        if self.wordclass:
            return '/'.join([self.baseurl, self.wordclass, self.word])
        else:
            return '/'.join([self.baseurl, self.word])


    def get_word_jsonData(self):
        response = requests.get(self.url).content
        jsonData = json.loads(response)
        if len(jsonData) > 1:
            raise Exception('found several words, please be more specific, exiting ...')
        return jsonData


    def convert_json_to_ordabokstruc(self):
        jsonData = self.get_word_jsonData()
        for beygingarmyndir in jsonData[0].get('bmyndir'):
            self.ord_dict[list(beygingarmyndir.values())[0]] = list(beygingarmyndir.values())[1]

        if jsonData[0].get('ofl') == 'no':
            self.wordclass = jsonData[0].get('ofl_heiti').lower()
            self.kyns = self.translate_abbrev.get(jsonData[0].get('kyn'))

            self.no_beygingarmyndir.setdefault('Nf',
                [self.ord_dict.get('NFET'),
                self.ord_dict.get('NFETgr'),
                self.ord_dict.get('NFFT'),
                self.ord_dict.get('NFFTgr')]
            )
            self.no_beygingarmyndir.setdefault('þf',
                [self.ord_dict.get('ÞFET'),
                self.ord_dict.get('ÞFETgr'),
                self.ord_dict.get('ÞFFT'),
                self.ord_dict.get('ÞFFTgr')]
            )
        elif jsonData[0]['ofl'] == 'so':
            self.so_beygingarmyndir.setdefault('Infinitiv', self.ord_dict.get('GM-NH'))

            self.so_beygingarmyndir.setdefault('Nútíð',
                [self.ord_dict.get('GM-FH-NT-1P-ET'),
                self.ord_dict.get('GM-FH-NT-2P-ET'),
                self.ord_dict.get('GM-FH-NT-3P-ET'),
                self.ord_dict.get('GM-FH-NT-1P-FT'),
                self.ord_dict.get('GM-FH-NT-2P-FT'),
                self.ord_dict.get('GM-FH-NT-3P-FT')]
            )
            self.so_beygingarmyndir.setdefault('Þátíð',
                [
                self.ord_dict.get('GM-FH-ÞT-1P-ET'),
                self.ord_dict.get('GM-FH-ÞT-2P-ET'),
                self.ord_dict.get('GM-FH-ÞT-3P-ET'),
                self.ord_dict.get('GM-FH-ÞT-1P-FT'),
                self.ord_dict.get('GM-FH-ÞT-2P-FT'),
                self.ord_dict.get('GM-FH-ÞT-3P-FT')
                ]
            )

def main():
    # word = arnastofnun('kók', 'no')
    word = arnastofnun(args.word, args.wordclass)
    word.convert_json_to_ordabokstruc()

    # Testausgaben
    try:
        pprint('kyns: {0}'.format(word.kyns))
        pprint(word.so_beygingarmyndir)
    except:
        pass
    try:
        pprint(word.no_beygingarmyndir)
        # pprint(word.no_beygingarmyndir.get('Nf'))
        # pprint(word.no_beygingarmyndir.get('þf'))
    except:
        pass


if __name__ == "__main__":

    parser = ArgumentParser()
    parser.add_argument("word")
    parser.add_argument("wordclass")
    args = parser.parse_args()

    main()
