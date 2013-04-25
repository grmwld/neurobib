#!/usr/bin/env python
# -*- coding:utf-8 -*-

import sys
import argparse


COMMON_WORDS = set('for a of the and to in we'.split())


class Corpus:
    def __init__(self, documents):
        self.__documents = documents
        
    def pre_process(self):
        all_tokens = sum(self.__documents, [])
        tokens_once = set(word for word in set(all_tokens) if all_tokens.count(word) == 1)
        for document in self.__documents:
            document.preproced = [[word for word in text if word not in tokens_once]
                                  for text in self.documents_text]

    @property
    def documents_text(self):
        return (document.text for document in self.__documents)

    @property
    def documents_preproced(self):
        return (document.preproced for document in self.__documents)

    def add_document(self, document):
        self.__documents.append(document)


class Document:
    def __init__(self, text, common_words=COMMON_WORDS):
        self.__text = [word for word in text.lower().strip().split() 
                       if word not in common_words]
        self.__preproced = self.__text[:]

    @property
    def text(self):
        return self.__text

    @property
    def preproced(self):
        return self.__preproced



def parse_bibliofile(infile):
    fields = set('PT AU AF CA TI SO SE ED LA DT CE DP SC DE ID AB C1 RP EM RI PU PI PA WP SN BN J9 JI PY PD VL IS PN SU SI BP EP PG DI GAi UT ER EF'.split())
    entry = dict.fromkeys(fields, [''])
    for i in range(2): infile.readline()
    flag_first = True
    while True:
        cur_line = infile.readline().strip()
        if cur_line == 'ER':
            entry[cur_field] = cur_value
            yield entry
            entry = dict.fromkeys(fields, [''])
        elif cur_line == 'EF':
            break
        elif cur_line == '':
            continue
        else:
            cur_line = cur_line.split('\t', 1)
            if len(cur_line) > 1:
                if cur_line[0] in fields:
                    if flag_first is False: entry[cur_field] = cur_value
                    flag_first = False
                    cur_field = cur_line[0]
                    cur_value = [cur_line[1]]
                else:
                    print >>sys.stderr, 'Unknown field ' + cur_field + ' in line : ' + str(cur_line)
            else:
                cur_value.append(cur_line[0])



def main():
    with open('./sss.txt', 'r') as infile:
        for i in parse_bibliofile(infile):
            print i


if __name__ == '__main__':
    main()
