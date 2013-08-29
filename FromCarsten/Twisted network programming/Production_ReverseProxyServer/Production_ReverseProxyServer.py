"""
This example demonstrates how to run a reverse proxy.

Run this example with:
    $ python reverse-proxy.py

Then visit http://localhost:8080/ in your web browser.
"""

from twisted.internet import reactor
from twisted.web import proxy, server
from twisted.web.resource import Resource

# Reverse Proxy
class ListenURL(Resource):
    isLeaf = False
    #for example http://localhost/test
    def getChild(self, name, request):
        if name == "traxis":
            print 'traxis'
            return proxy.ReverseProxyResource('www.yahoo.com', 80, '')
        else:
            print 'else'
            return proxy.ReverseProxyResource('www.google.be', 80, '')
        
site = server.Site(ListenURL())
reactor.listenTCP(12345, site)
reactor.run()

