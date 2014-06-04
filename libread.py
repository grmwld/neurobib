#!/usr/bin/env python
# -*- coding:utf-8 -*-

import sys
import argparse
import xml.etree.ElementTree as ET


class EndNote_Parser:
    def __init__(self):
        self.__fields = set('PT AU AF CA TI SO SE ED LA DT CE DP SC DE ID AB C1 RP EM RI PU PI PA WP SN BN J9 JI PY PD VL IS PN SU SI BP EP PG DI GAi UT ER EF'.split()) 

    def parse(self, infile):
        entry = dict.fromkeys(self.__fields, [''])
        flag_first = True
        while True:
            cur_line = infile.readline().strip()
            if cur_line == 'ER':
                entry[cur_field] = cur_value
                yield entry
                entry = dict.fromkeys(self.__fields, [''])
            elif cur_line == 'EF':
                break
            elif cur_line == '':
                continue
            else:
                cur_line = cur_line.split('\t', 1)
                if len(cur_line) > 1:
                    if cur_line[0] in self.__fields:
                        if flag_first is False:
                            entry[cur_field] = ' '.join(cur_value)
                        flag_first = False
                        cur_field = cur_line[0]
                        cur_value = [cur_line[1]]
                    else:
                        print >>sys.stderr, 'Unknown field ' + cur_field + ' in line : ' + str(cur_line)
                else:
                    cur_value.append(cur_line[0])


class Pubmed_XML_parser:
    def __init__(self):
        pass

    def parse(self, infile):
        #TODO: Build dictionary while retainig depth levels (go through)
        #      children nodes recursively
        tree = ET.iterparse(infile, ['start', 'end'])
        entry = {}
        for event, elem in tree:
            if event == 'start' and elem.tag == 'PubmedArticle':
                entry = {}
            if event == 'end':
                if elem.tag == 'PubmedArticle':
                    yield entry
                else:
                    if elem.tag in entry:
                        entry[elem.tag].append(elem.text)
                    else:
                        if elem.text and elem.text.strip() != '':
                            entry[elem.tag] = [elem.text]



def main(args):
    pass


if __name__ == '__main__':
    main()
