'''
Created on Sep 14, 2012

@author: carsten
'''
import re
import urllib

#open file and create Regular Expression for the bible example
f = open(r'tim.txt', 'r')

#Set up regular expressions to normalize queries
regex = re.compile(r'Line.*invalid syntax')

nf = open('newTim.txt', 'w+')
for line in f:
    invalidSyntaxCount = regex.findall(line)
    print len(invalidSyntaxCount)
    if len(invalidSyntaxCount) != 1:
        nf.write(line)