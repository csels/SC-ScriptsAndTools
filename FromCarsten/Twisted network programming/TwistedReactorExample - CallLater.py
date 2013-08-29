'''
Created on Jun 26, 2013

@author: csels
'''
import sys
from twisted.internet import reactor
 
def callfunc(x):
    print x
    
reactor.callWhenRunning(callfunc, "Test123")
reactor.run()