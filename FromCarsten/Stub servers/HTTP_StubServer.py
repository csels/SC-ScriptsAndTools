'''
Created on May 8, 2013

@author: csels
'''
import BaseHTTPServer
PORT_NUMBER = 8080

#This class will handles any incoming request from
#the browser 
class myHandler(BaseHTTPServer.BaseHTTPRequestHandler):
    #Handler for the GET requests
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type','text/html')
        self.end_headers()
        
        # Send the html message
        self.wfile.write(r'<?xml version="1.0" encoding="UTF-8"?><cpi:Content xmlns:cpi="urn:eventis:cpi:1.0" id="ffffffff-ffff-ffff-ffff-ffffffffffff"><cpi:Status id="IngestedAndPlayable"><cpi:IngestPercentage>0</cpi:IngestPercentage></cpi:Status></cpi:Content>')
        return
    
    def do_PUT(self):
        self.send_response(200)
        self.send_header('Content-type','text/html')
        self.end_headers()
        
        # Send the html message
        self.wfile.write(r'HTTP/1.0 PUT OK')
        return

try:
    #Create a web server and define the handler to manage the
    #incoming request
    server = BaseHTTPServer.HTTPServer(('', PORT_NUMBER), myHandler)
    print 'Started httpserver on port ', PORT_NUMBER
    
    #Wait forever for incoming htto requests
    server.serve_forever()
    
except KeyboardInterrupt:
    print '^C received, shutting down the web server'
    server.socket.close()