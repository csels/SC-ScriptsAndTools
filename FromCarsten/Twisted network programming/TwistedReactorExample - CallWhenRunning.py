'''
Created on Jun 26, 2013

@author: csels
This example will call the event handler which is associated with the reactor after 4 seconds
'''
import sys
from twisted.internet import reactor
 
def callfunc(x):
    print x
    
reactor.callLater(4, callfunc, "Test")
reactor.run()