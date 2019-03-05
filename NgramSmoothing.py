#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar  2 18:37:54 2019
Ngram with interpolation smoothing method fine-tuned by EM algorithm on dev
@author: yuedai
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import collections

class Ngram(object):
    """N-gram language model class."""

    def __init__(self):
        self.counts = [1]
        self.total_count = [0]
        self.para = [0]
        self.n = 0

    def train(self, n, filename):
        """Train the model on a text file."""
        
        #initialize hyperparameters
        init = 1 / (n + 1)
        self.para[0] = init  
        
        self.n = n
        
        for k in range(1, n + 1):
            self.para.append(init)
            self.counts.append(collections.Counter())
            self.total_count.append(0)
            for line in open(filename):
                samp = line.rstrip('\n')
#                samp = '~' + samp + '~'
                for i in range(len(samp) - k):
                    w = samp[i:i + k]
                    self.counts[k][w] += 1
                    self.total_count[k] += 1
                    
        self.total_count[0] = self.total_count[1]        

    def start(self):
        """Reset the state to the initial state."""
        pass

    def read(self, w):
        """Read in character w, updating the state."""
        pass
    
    def prob(self, k, w):
        """Return the probability of the next character being w given the
        current state."""
        if k == 0:
            return 1/self.total_count[0];
        return self.counts[k][w] / self.total_count[k]
    
    def probMod(self, w):
        """Return the probability of the next character being w given the
        current state with smoothing"""
        res = self.para[0] * 1/self.total_count[0]
        for i in range(1, len(self.counts)):
            q = w[-i:]
            res = res + self.para[i] * self.prob(i, q)
        return res

    def pred(self, w):
        """Do the prediction with maximum N - 1 characters given, if unknown in put
        given will return '*' as an unknown token"""
        pr = 0;
        res = ''
        for item in self.counts[self.n]:
            if w in item[:-1] and self.probMod(item) > pr:
#                print("HIT")
#                print(item)
                i = item.index(w) + len(w)
                res = item[i]
                pr = self.probMod(item)
        if res == '':
            res = '*'
        return res


    def smoothing(self, p):
#        reset hyperparameters
#        init = p
#        for i in range(len(self.para)):
#            self.para[i] = init
        
        self.para[-1] = p
        re = 1 - p
        for i in range(2, len(self.para)):
#            print(i)
            self.para[-i] = re * p
            re = re * (1 - p)
            
        self.para[0] = re
#        #tuning parameters based on dev data
#        expC = []
#        for i in range(len(self.para)):
#            expC.append(0)
#            
#        thread = 1
#        while thread == 1:
#            thread = 0
#            
#            for i in range(len(expC)):
#                expC[i] = 0
#            
#            for j in range(len(expC)):
##                print(j)
#                for line in open(filename):
#                    samp = line.rstrip('\n')
#                    samp = '~' + samp + '~'
#                    for i in range(self.n, len(samp)):
#                        wN = samp[i - self.n: i]
#                        w = samp[i + self.n - 1 - j:i + self.n - 1]
##                        print(w)
##                        print(wN)
##                        print(self.prob(j, w))
#                        expC[j] = expC[j] + self.para[j] * self.prob(j, w)/self.probMod(wN)
#            
#            print(expC)
#            
#            for j in range(len(self.para)):
#                nextPara = expC[j] / sum(expC)
#                delta = abs(nextPara - self.para[j])
#                if delta > 0.05:
#                    thread = 1
#                self.para[j] = nextPara
                
        print("Hyper Parameters:" + str(self.para))
    
    def test(self, filename):
        """Test Ngram module with test data, return overall accuracy."""
        n = self.n
        hit = 0
        total = 0
        
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
            
        