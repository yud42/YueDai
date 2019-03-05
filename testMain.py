#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 28 16:41:31 2019

@author: yuedai
"""
import sys
import NgramVanilla as ngram

if __name__ == "__main__":
    
    n = int(sys.argv[1])
    trainFile = sys.argv[2]
    testFile = sys.argv[3]
#    trainFile = './english/train'
#    testFile = './english/dev'
#    for k in range(1,10):
#        k = 3
#        n = k
        
    m = ngram.Ngram()
    m.train(n,trainFile)
    
    accu = m.test(testFile)
    print('The final accuracy of ' + str(n) + '-gram model is: ' + str(accu))
    