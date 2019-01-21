# -*- coding: utf-8 -*-
"""
Created on Tue Dec  4 23:26:59 2018

@author: latti
"""

import pickle

occurance = pickle.load(open("occurance10a.p", "rb"))

s = [(k, occurance[k]) for k in sorted(occurance, key=occurance.get, reverse=True)]
count = 0
for k, v in s:
    if count >= 10:
        break
    print(k + ":" + str(v))
    count = count + 1