"""
This example demonstrates how to run a reverse proxy.

Run this example with:
    $ python reverse-proxy.py

Message of the day server
"""
from twisted.internet.protocol import Factory, Protocol
from twisted.internet import reactor

class QOTD(Protocol):
    def connectionMade(self):
        self.transport.write(self.factory.quote+'\r\n')
        self.transport.loseConnection()
        
class QOTDFactory(Factory):
    protocol = QOTD
    def __init__(self, quote=None):
        self.quote = quote or 'An apple a day keeps the doctor away'

reactor.listenTCP(8007, QOTDFactory("configurable quote"))
reactor.run()