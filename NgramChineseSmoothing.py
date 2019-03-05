#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import collections

class Ngram(object):
    """N-gram language model class with smoothing."""

    def __init__(self):
        self.counts = [1]
        self.total_count = [0]
        self.para = [0]
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
        
        #initialize hyperparameters
        init = 1 / (n + 1)
        self.para[0] = init  
        
        self.n = n
        
        for k in range(1, n + 1):
            self.para.append(init)
            self.counts.append(collections.Counter())
            self.total_count.append(0)
            for sent in open(filename):
                sent = sent.rstrip('\n')
#                sent = '<ST> ' + sent + ' <END>'
                samp = sent
                for i in range(len(samp) - k):
                    w = samp[i:i + k]
                    self.counts[k][w] += 1
                    self.total_count[k] += 1
                    
        self.total_count[0] = self.total_count[1] 

#    def train(self, n, filename):
#        """Train the model on a text file."""
#        self.n = n
#        for sent in open(filename):
#            sent = sent.rstrip('\n')
#            sent = '<ST> ' + sent + ' <END>'
#            samp = sent
##            samp = sent.split()
#            for i in range(len(samp) - n):
#                w = samp[i:i + n]
#                self.counts[w] += 1
#                self.total_count += 1

    def start(self):
        """Reset the state to the initial state."""
        pass

    def read(self, w):
        """Read in character w, updating the state."""
        pass
    
    def trans(self, w):
        if w == '<ST>' or w == '<END>': return w
        return self.pinyinmap[w]
     
    def prob(self, k, w):
        """Return the probability of the next character being w given the
        current state."""
        if k == 0:
            return 1/self.total_count[0];
        return self.counts[k][w] / self.total_count[k]

#    def prob(self, w):
#        """Return the probability of the next character being w given the
#        current state."""
#        return self.counts[w] / self.total_count
        
    def probMod(self, w):
        """Return the probability of the next character being w given the
        current state with smoothing"""
        res = self.para[0] * 1/self.total_count[0]
        for i in range(1, len(self.counts)):
            q = w[-i:]
            res = res + self.para[i] * self.prob(i, q)
        return res
    
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
#            print(q)
            prob = self.probMod(q)
#            print(prob)
            if prob > pr:
#                print("HIIIT")
                res = han
                pr = prob
        
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
                        
        