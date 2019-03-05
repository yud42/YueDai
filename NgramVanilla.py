#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import collections

class Ngram(object):
    """N-gram language model class."""

    def __init__(self):
        self.counts = collections.Counter()
        self.total_count = 0
        self.n = 0

    def train(self, n, filename):
        """Train the model on a text file."""
        self.n = n
        for line in open(filename):
            samp = line.rstrip('\n')
#            samp = '~' + samp + '~'
            for i in range(len(samp) - n):
                w = samp[i:i + n]
                self.counts[w] += 1
                self.total_count += 1

    def start(self):
        """Reset the state to the initial state."""
        pass

    def read(self, w):
        """Read in character w, updating the state."""
        pass

    def prob(self, w):
        """Return the probability of the next character being w given the
        current state."""
        return self.counts[w] / self.total_count
    
    def pred(self, w):
        """Do the prediction with maximum N - 1 characters given, if unknown in put
        given will return '*' as an unknown token"""
        pr = 0;
        res = ''
        for item in self.counts:
            if w in item[:-1] and self.prob(item) > pr:
#                print("HIT")
#                print(item)
                i = item.index(w) + len(w)
                res = item[i]
                pr = self.prob(item)
        if res == '':
            res = '*'
        return res
    
    def test(self, filename):
        """Test Ngram module with test data, return overall accuracy."""
        hit = 0
        total = 0
        n = self.n
        for sent in open(filename):
            samp = sent.rstrip('\n')
#            samp = '~' + samp + '~' 
            for i in range(len(samp) - n):
                total = total + 1
                prev = samp[i:i + n - 1]
                pred = self.pred(prev)
                if pred == samp[i + n - 1]:
                    hit = hit + 1
                     
        return hit/total
            
        