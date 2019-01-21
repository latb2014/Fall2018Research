# -*- coding: utf-8 -*-
"""
Created on Tue Dec  4 23:26:59 2018

@author: latti
"""

import pickle

levels = pickle.load(open("levels10a.p", "rb"))

values = list(levels.values())

one = 0
two = 0
three = 0

for number in values:
    if number == 1:
        one = one + 1
    if number == 2:
        two = two + 1
    if number == 3:
        three = three + 1
        
print("ONE: " + str(one) + "\nTWO: " + str(two) + "\nTHREE: " + str(three))