'''
Created on Nov 26, 2012

@author: csels
'''
import sys
import re

data = open(sys.argv[1],'r').read()

fields = re.split('(<.*?>)',data)
level = 0
for f in fields:
   if f.strip() == '': continue
   if f[0]=='<' and f[1] != '/':
       print ' '*(level*4) + f
       level = level + 1
       if f[-2:] == '/>':
           level = level - 1
   elif f[:2]=='</':
       level = level - 1
       print ' '*(level*4) + f
   else:
       print ' '*(level*4) + f