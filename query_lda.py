#!/usr/bin/env python
# -*- coding:utf-8 -*-

import sys
import argparse
from gensim import corpora, models
from libcorpus import Corpus



def main(args):

    lda = models.LdaModel.load(args.model)

    for i in lda.show_topics(topics=-1, log=False):
        print i

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-m', '--model', dest='model',
        help='Input file'
    )
    parser.add_argument(
        '-o', '--outfile', dest='outfile',
        type=argparse.FileType('w'),
        nargs='?',
        default=sys.stdout,
        help='Output file'
    )
    main(parser.parse_args())
