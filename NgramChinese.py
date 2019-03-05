#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import collections

class Ngram(object):
    """N-gram language model class."""

    def __init__(self):
        self.counts = collections.Counter()
        self.total_count = 0
        self.n = 0
        self.pinyinmap = {}
    
    def setpinyin(self, filename):
        for line in open(filename):
            pair = line.split()
            if pair[1] in self.pinyinmap:
                self.pinyinmap[pair[1]].append(pair[0])
            else:
                self.pinyinmap[pair[1]] = [pair[0]] 

    def train(self, n, filename):
        """Train the model on a text file."""
        self.n = n
        for sent in open(filename):
            sent = sent.rstrip('\n')
            sent = '<ST> ' + sent + ' <END>'
            samp = sent
#            samp = sent.split()
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
    
    def trans(self, w):
        if w == '<ST>' or w == '<END>': return w
        return self.pinyinmap[w]
     
    def prob(self, w):
        """Return the probability of the next character being w given the
        current state."""
        return self.counts[w] / self.total_count
    
    def pred(self, w, context):
        """Do the prediction with maximum N - 1 characters given, if unknown in put
        given will return '*' as an unknown token"""
        if(len(w) == 1): return w
        if(w == '<space>'): return ' '
        
        pr = 0
        res = ''
        cc = ''
        for c in context:
            cc = cc + c
        candidate = self.trans(w)
        for han in candidate:
            q = cc + han
            if self.prob(q) > pr:
                res = han
                pr = self.prob(q)
        
        if res == '':
            res = '<UNKNOWN>'
        
        return res
        

#        for item in self.counts:
#            if w in item[:-1] and self.prob(item) > pr:
##                print("HIT")
##                print(item)
#                i = item.index(w) + len(w)
#                res = item[i]
#                pr = self.prob(item)
#        if res == '':
#            res = '*'
#        return res
    
    def test(self, filenamePinyin, filenameHan):
        """Test Ngram module with test data, return overall accuracy."""
        hit = 0
        total = 0
        n = self.n
        samp1 = []
        for line in open(filenamePinyin):
            line = line.rstrip('\n')
#            sent = '<ST> ' + sent + ' <END>'
            line = line.split()
            for k in line:
                samp1.append(k)
#        print(len(samp1))
        samp2 = []
        for line in open(filenameHan):
            line = line.rstrip('\n')
        #    print(sent)
#            line = line.split()
            for t in line:
                for c in t:
                    samp2.append(c)
        #    samp = sent.split()
        #    samp2 = sent.split()
#            samp2 = ['<ST>'] + samp2 + ['<END>']
#        print(len(samp2))
#        print(samp1)
#        print(samp2)
        for i in range(n - 1, len(samp1)):
            total += 1
            w = samp1[i]
            context = samp2[i - (n - 1):i]
            pre = self.pred(w, context)
#            print(pre)
#            print(samp2[i])
            if pre == samp2[i]:
                hit += 1
                
                
        return hit/total
            
        