'''
Created on May 8, 2013

@author: csels
'''
from socket import *
import thread
import re
 
HOST = '127.0.0.1'# must be input parameter @TODO
PORT = 554 # must be input parameter @TODO

#RESPONSE DEFINITIONS
RESPONSE_SETUP = "Session: 635074309430563948\r\n\
Date: 2013-06-21T15:02:23Z\r\n\
Duration: 100\r\n\
Channel: Tsid=0;Svcid=1\r\n\
Tuning: frequency=00010000;symbol_rate=0000687;modulation=5;fec_inner=0;fec_outer=0\r\n\r\n"

RESPONSE_DESCR = "Public: OPTIONS, DESCRIBE, SETUP, TEARDOWN, PLAY, PAUSE, GET_PARAMETER\r\n\
Content-Type: application/sdp\r\nContent-Length: 177\r\n\r\n\
v=0\r\no=- 173050 0 IN IP4 62.65.253.102\r\n\
s=RTSP Session\r\n\
t=0 0\r\n\
c=IN IP4 62.65.253.102\r\n\
b=AS:8586.000\r\n\
a=type:vod\r\n\
a=range:npt=0-139\r\n\
m=video 0 UDP 33\r\n\
m=video 0 RTP/AVP/UDP 33\r\n\r\n"

RESPONSE_TEARDOWN = "Session: 635074309430563948\r\n\
Range: npt=3440-\r\n\r\n"
 
def handler(clientsock,clientaddr):
    while True:
        #Receive data from connected client socket
        data = clientsock.recv(1024)
        print data
        if data:
            print data
            #Find out the CSEQ no of the REQUEST and use in response
            patternCSEQ = re.compile(r'CSeq: (\d+)', re.MULTILINE)
            seqNo = re.findall(patternCSEQ, data)
            
            #Find out which RTSP Request is sent
            patternRTSP = re.compile(r'.*RTSP/1.0.*', re.MULTILINE)
            rtspRequest = re.findall(patternRTSP, data)
            
            #SET RTSP Response based on RTSP Request
            if re.findall(re.compile(r'.*SETUP.*', re.MULTILINE), rtspRequest[0]) != []:
                RESPONSE = "RTSP/1.0 200 OK\r\nCSeq: %s\r\n" % seqNo[0] + RESPONSE_SETUP
                print 'SETUP'
            elif re.findall(re.compile(r'.*PLAY.*', re.MULTILINE), rtspRequest[0]) != []:
                RESPONSE = 'RTSP/1.0 200 OK\r\nCSeq: %s\r\n\r\n' % seqNo[0]
                print 'PLAY'
            elif re.findall(re.compile(r'.*GET_PARAMETER.*', re.MULTILINE), rtspRequest[0]) != []:
                RESPONSE = 'RTSP/1.0 200 OK\r\nCSeq: %s\r\n\r\n' % seqNo[0]
                print 'GET_PARAMETER'
            elif re.findall(re.compile(r'.*DESCRIBE.*190/ RTSP/1.0$', re.MULTILINE), rtspRequest[0]) != []:
                RESPONSE = 'RTSP/1.0 400 Bad Request\r\nServer: Orbit2x\r\nCSeq: 5050\r\n\r\n' % seqNo[0]
                print 'DESCRIBE ERROR'
            elif re.findall(re.compile(r'.*DESCRIBE.*', re.MULTILINE), rtspRequest[0]) != []:
                RESPONSE = 'RTSP/1.0 200 OK\r\nServer: Orbit2x\r\nCSeq: %s\r\n' % seqNo[0] + RESPONSE_DESCR
                print 'DESCRIBE'
            elif re.findall(re.compile(r'.*TEARDOWN.*', re.MULTILINE), rtspRequest[0]) != []:
                RESPONSE = 'RTSP/1.0 200 OK\r\nServer: Orbit2x\r\nCSeq: %s\r\n\r\n' % seqNo[0] + RESPONSE_TEARDOWN
                print 'TEARDOWN'
                
            #Send the appropriate RESPONSE back
            print 'sent: %s' % RESPONSE
            clientsock.send(RESPONSE) 
        else:
            break
        
    #Close socket
    clientsock.close()
 
if __name__=='__main__':
    #Initialize server socket  with appropriate modes
    s = socket(AF_INET, SOCK_STREAM)
    s.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    
    #Bind server to a IP/Port tuple and allow multiple connects
    s.bind((HOST, PORT))
    s.listen(5)
    
    #Set up continuous loop to listen for connections and print connected ip's
    while True:
        print 'waiting for connection...'
        clientsock, clientaddr = s.accept()
        print '...connected from:', clientaddr
        
        #Start new thread per connected client socket
        thread.start_new_thread(handler, (clientsock, clientaddr))