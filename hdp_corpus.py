#!/usr/bin/env python
# -*- coding:utf-8 -*-

import sys
import argparse
from gensim import corpora, models, similarities
from libcorpus import Corpus


def main(args):
    corpus = Corpus()

    corpus.load(args.corpus_file, args.dictionary_file)

    model = corpus.transform(args.model, args.num_topics, args.num_passes)

    model.save(args.outfile)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-c', '--corpus_file', dest='corpus_file',
        help='Corpus file'
    )
    parser.add_argument(
        '-d', '--dictionary_file', dest='dictionary_file',
        help='Dictionary file'
    )
    parser.add_argument(
        '-o', '--outfile', dest='outfile',
        help='Output file'
    )
    parser.add_argument(
        '-n', '--num_topics', dest='num_topics',
        type=int,
        default=10,
        help='Number of topics (if applicable)'
    )
    parser.add_argument(
        '-p', '--num_passes', dest='num_passes',
        type=int,
        default=1,
        help='Number of passes'
    )
    parser.add_argument(
        '-m', '--model', dest='model',
        choices=['hdp', 'lda'],
        default='lda',
        help='help'
    )
    main(parser.parse_args())
