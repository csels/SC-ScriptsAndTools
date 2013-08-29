'''
Created on Jun 26, 2013

@author: csels
'''
import sys
from twisted.protocols.basic import LineReceiver
from twisted.internet import reactor
from twisted.internet.protocol import Protocol
from twisted.internet.protocol import ServerFactory
from twisted.python import log


class MyProtocol(LineReceiver):
    delimiter = '\n'
    def connectionMade(self):
        self.client_ip = self.transport.getPeer()
        log.msg("Client connection from %s" % self.client_ip)
        self.factory.clients.append(self.client_ip)
        if len(self.factory.clients) > 2:
            print '2 clients are already connected. Aborting connection.'
            self.transport.write("2 clients are already connected. Aborting connection.")
            self.transport.loseConnection()
    def connectionLost(self, reason):
        self.client_ip = self.transport.getPeer()
        log.msg("Disconnect from %s" % self.client_ip)
        self.factory.clients.remove(self.client_ip)
    def lineReceived(self, line):
        print 'Line received: %s' % line
        
class MyFactory(ServerFactory):
    protocol = MyProtocol
    def __init__(self):
        self.clients = []
        

log.startLogging(sys.stdout)
reactor.listenTCP(8093, MyFactory())
reactor.run()