#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 28 16:10:04 2019

@author: yuedai
"""

#a = "abcdefg hijklmn"
#n = 4
#b = a.rstrip('n')
#for i in range(len(b) - n):
#    t = ''
#    for j in range(n):
#        t = t + b[i + j]
##    if i <= len(b) - n:
##        for j in range(n):
##            t = t + b[i + j]
##    else:
##        for j in range(len(b)-i):
##            t = t + b[i + j]
##        break
##    print(t)
#sub = 'defg'    
#print(sub[-2:-1])
pinyinmap = {}

for line in open("./chinese/charmap"):
    pair = line.split()
    if pair[1] in pinyinmap:
        pinyinmap[pair[1]].append(pair[0])
    else:
        pinyinmap[pair[1]] = [pair[0]] 

print(pinyinmap['tian'])

samp1 = []
for sent in open("./chinese/test.pin"):
    sent = sent.rstrip('\n')
    sent = '<ST> ' + sent + ' <END>'
    samp1 = sent.split()

print(len(samp1))

samp2 = []
for sent in open("./chinese/test.han"):
    samp2 = []
    sent = sent.rstrip('\n')
#    print(sent)
    for t in sent:
        samp2.append(t)
#    samp = sent.split()
#    samp2 = sent.split()
    samp2 = ['<ST>'] + samp2 + ['<END>']
print(len(samp2))

cc = ''
for c in samp2:
    cc = cc + c
print(cc)

file = open("./chinese/test.han").read()
print(len(file))


a = "abcd"
b = ['a', 'b', 'c', 'd']
l = len(a) - 1
hit = 0
for i in range(l):
    if a[i] == b[i]: hit+=1

print(hit/len(a))
#print(pinyinmap)
