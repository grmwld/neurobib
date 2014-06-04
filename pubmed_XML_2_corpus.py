#!/usr/bin/env python
# -*- coding:utf-8 -*-

import sys
import argparse
from libcorpus import Corpus, Document
from libread import Pubmed_XML_parser


def main(args):

    parser = Pubmed_XML_parser()
 
    corpus = Corpus()

    for entry in parser.parse(args.infile):
        corpus.add_document(Document(entry['AbstractText'][0]))

    corpus.process(args.no_below, args.no_above)

    corpus.save(args.outfile)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-i', '--infile', dest='infile',
        type=argparse.FileType('r'),
        nargs='?',
        default=sys.stdin,
        help='Input file'
    )
    parser.add_argument(
        '-o', '--outfile', dest='outfile',
        help='Output file'
    )
    parser.add_argument(
        '-b', '--no_below', dest='no_below',
        type=int,
        default=5,
        help='Do not keep tokens appearing in less than N documents'
    )
    parser.add_argument(
        '-a', '--no_above', dest='no_above',
        type=float,
        default=0.6,
        help='Do not keep tokens appearing in more than N*100 percent of total documents'
    )
    main(parser.parse_args())
