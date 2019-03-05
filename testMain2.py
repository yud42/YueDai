#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 28 16:41:31 2019

@author: yuedai
"""
import sys
import NgramSmoothing as ngram
import NgramVanilla as ngramV

if __name__ == "__main__":
    
#    n = int(sys.argv[1])
#    trainFile = sys.argv[2]
#    testFile = sys.argv[3]
    for k in range(5,10):    
        n = k
        trainFile = './english/train'
        devFile = './english/dev'
        testFile = './english/test'
        
        v = ngramV.Ngram()
        v.train(n, trainFile)
        
        m = ngram.Ngram()
        m.train(n, trainFile)
        
    #    for i in range(0,11):
            
        m.smoothing(0.1 * 5)
        
    #    p = m.prob('a')
    #    print(p)
    #    w = ''
    #    print(w=='')
    #    a = m.pred('~')
    #    print(a)
        
        
        accuv = v.test(testFile)
        accu = m.test(testFile)
        print('The final accuracy of ' + str(n) + '-gram model is: ' + str(accuv))
        print('The final accuracy of ' + str(n) + '-gram model with interpolation is: ' + str(accu))