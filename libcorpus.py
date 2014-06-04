#!/usr/bin/env python
# -*- coding:utf-8 -*-

import sys
import argparse
import re
import itertools
from gensim import corpora, models, similarities
from gensim import utils
from preprocessing import preprocess_string

import logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)


COMMON_WORDS = set('an c elsevier for a of the and to in we is are have on by'.split())

WHITELIST_CHARS = re.compile('[^a-zA-Z0-9 ]+')


class Corpora_Dictionary(corpora.Dictionary):
    def __init__(self, *args, **kwargs):
        super(Corpora_Dictionary, self).__init__(*args, **kwargs)

    def doc2bow(self, document, allow_update=False, return_missing=False, include_zero=False):
        result = dict.fromkeys(self.keys(), 0) if include_zero else {}
        missing = {}
        document = sorted(document)
        # construct (word, frequency) mapping. in python3 this is done simply
        # using Counter(), but here i use itertools.groupby() for the job
        for word_norm, group in itertools.groupby(document):
            frequency = len(list(group)) # how many times does this word appear in the input document
            tokenid = self.token2id.get(word_norm, None)
            if tokenid is None:
                # first time we see this token (~normalized form)
                if return_missing:
                    missing[word_norm] = frequency
                if not allow_update: # if we aren't allowed to create new tokens, continue with the next unique token
                    continue
                tokenid = len(self.token2id)
                self.token2id[word_norm] = tokenid # new id = number of ids made so far; NOTE this assumes there are no gaps in the id sequence!
            # update how many times a token appeared in the document
            result[tokenid] = frequency
        if allow_update:
            self.num_docs += 1
            self.num_pos += len(document)
            self.num_nnz += len(result)
            # increase document count for each unique token that appeared in the document
            for tokenid in result.iterkeys():
                self.dfs[tokenid] = self.dfs.get(tokenid, 0) + 1
        # return tokenids, in ascending id order
        result = sorted(result.iteritems())
        if return_missing:
            return result, missing
        else:
            return result


class Corpus:
    def __init__(self, documents=[]):
        self.__documents = documents
        self.__bag_of_word = None
        
    def process(self, no_below=5, no_above=0.6):
        self.__dictionary = Corpora_Dictionary(self.documents_pre_processed)
        self.__dictionary.filter_extremes(no_below=no_below, no_above=no_above, keep_n=None)

    def transform(self, model='lda', ntopics=1, num_passes=1):
        #tfidf = models.TfidfModel(corpus=self.bag_of_word)
        #corpus_tfidf = tfidf[self.bag_of_word]
        ##return corpus_tfidf

        if model == 'lda':
            return models.LdaModel(self.bag_of_word, num_topics=ntopics, id2word=self.__dictionary, passes=num_passes, chunksize=10000, update_every=0, distributed=True)
        elif model == 'hdp':
            return models.HdpModel(self.bag_of_word, id2word=self.__dictionary)

    @property
    def documents_text(self):
        return (document.text for document in self.__documents)

    @property
    def documents_pre_processed(self):
        return (document.pre_processed for document in self.__documents)

    @property
    def dictionary(self):
        return self.__dictionary

    @property
    def bag_of_word(self):
        if self.__bag_of_word is None:
            return (self.__dictionary.doc2bow(text, include_zero=False)
                    for text in self.documents_pre_processed)
        else:
            return self.__bag_of_word

    @bag_of_word.setter
    def bag_of_word(self, value):
        if self.__bag_of_word is None:
            self.__bag_of_word == value

    def add_document(self, document):
        self.__documents.append(document)

    def save(self, filename):
        dict_fname= '.'.join([filename, 'dict'])
        corpus_fname = '.'.join([filename, 'mm'])
        self.__dictionary.save(dict_fname)
        corpora.MmCorpus.serialize(corpus_fname, self.bag_of_word)

    def load(self, corpus_fname, dictionary_fname):
        self.__dictionary = corpora.Dictionary.load(dictionary_fname)
        self.bag_of_word = corpora.MmCorpus(corpus_fname)
        


class Document:
    def __init__(self, text, common_words=COMMON_WORDS, whitelist_chars=WHITELIST_CHARS):
        self.__text = text
        #self.__preprocessed = utils.lemmatize(text)
        self.__preprocessed = preprocess_string(text) 

    def __str__(self):
        return ' '.join(self.text)

    @property
    def text(self):
        return self.__text

    @property
    def pre_processed(self):
        return self.__preprocessed




def main():

    from libread import Pubmed_XML_parser as pmxml
    from libread import EndNote_Parser as EN

    corpus = Corpus()

    #en_parser = EN()

    #with open('./sss2000-full.txt', 'r') as infile:
        #for i in en_parser.parse(infile):
            #if len(i['AB']) > 1:
                #corpus.add_document(Document(i['AB']))


    ##for i in corpus.bag_of_word:
        ##print i
    ##for i in corpus.transform():
        ##print i
    ##for i in corpus.transform(2):
        ##print i[0][1], i[1][1]
    #w = list(corpus.transform(2))
    #for i in range(40):
        #print w[i]


    xml_parser = pmxml()
    
    for entry in xml_parser.parse('./pubmed_result.xml'):
        corpus.add_document(Document(entry['AbstractText'][0]))

    print 'done reading file'

    corpus.process()

    print 'done processing'

    w = list(corpus.transform(20))
    for i in range(40):
        print w[i]
    


if __name__ == '__main__':
    main()
