'''
Created on Jun 26, 2013

@author: csels
'''
import sys
from twisted.web.server import Site
from twisted.web.resource import Resource
from twisted.internet import reactor

class norbro3d(Resource):
    def render_GET(self, request):
        return 'GET'
    def render_PUT(self, request):
        HTTPBody = request.content.getvalue()
        return 'PUT \r\n%s' % HTTPBody

#Define path for the web service        
root = Resource()
root.putChild("test", norbro3d())
factory = Site(root)

reactor.listenTCP(8880, factory)
reactor.run()