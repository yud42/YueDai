#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Mar  3 17:29:31 2019

@author: yuedai
"""

import sys
import NgramChinese as ngram
import NgramChineseSmoothing as ngramMod

if __name__ == "__main__":
    
    n = int(sys.argv[1])
    trainFile = sys.argv[2]
    testFilePin = sys.argv[3]
    testFileHan = sys.argv[4]
    charmap = sys.argv[5]
    
#    trainFile = './chinese/train.han'
#    testFilePin = './chinese/test.pin'
#    testFileHan = './chinese/test.han'
#    charmap = "./chinese/charmap"
#    for k in range(1,10):
#    k = 3
#    n = k
#    
    v = ngram.Ngram()
    v.setpinyin(charmap)
    v.train(n,trainFile)
    
    m = ngramMod.Ngram()
    m.setpinyin(charmap)
    m.train(n,trainFile)
    m.smoothing(0.1 * 9)
    
    accu = v.test(testFilePin, testFileHan)
    accum = m.test(testFilePin, testFileHan)
    print('The final accuracy of ' + str(n) + '-gram model is: ' + str(accu))
    print('The final accuracy of ' + str(n) + '-gram model with smoothing is: ' + str(accum))
    
