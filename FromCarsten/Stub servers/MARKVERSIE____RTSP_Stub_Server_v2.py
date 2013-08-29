'''
Created on May 8, 2013

@author: csels
'''
from socket import *
from random import randrange
import thread, re, os, time
import argparse

parser = argparse.ArgumentParser(description='RTSP Stub Server.')
parser.add_argument('listen_address', metavar='ip', nargs='?', default='0.0.0.0', help='The ip the server should bind to.')
parser.add_argument('listen_port', metavar='port', nargs='?', default='554', type=int, help='The port the server should listen on.')
args = parser.parse_args()

sessionDb = 'sessions\\'



#rtspResponse DEFINITIONS
responseOk = '''
RTSP/1.0 200 OK
CSeq: %s
Date: %s
Server: Broadbus RTSP Server

'''

responseBadRequest = '''
RTSP/1.0 400 Bad Request
CSeq: %s
Date: %s
Server: Broadbus RTSP Server
'''

responseInternalServerError = '''
RTSP/1.0 500 Internal Server Error
Server: Broadbus RTSP Server
CSeq: %s

'''
responseSessionNotFound = '''
RTSP/1.0 454 Session Not Found
CSeq: %s
Session: %s
Date: %s
Server: Broadbus RTSP Server

'''

responseSetup = '''
RTSP/1.0 200 OK
CSeq: %s
Session: %s
Date: %s
Server: Broadbus RTSP Server
Duration: 100
Channel: Tsid=0;Svcid=1
Tuning: frequency=00010000;symbol_rate=0000687;modulation=5;fec_inner=0;fec_outer=0

'''

responseDescribe = '''
RTSP/1.0 200 OK
CSeq: %s
Date: %s
Server: Broadbus RTSP Server
Public: OPTIONS, DESCRIBE, SETUP, TEARDOWN, PLAY, PAUSE, GET_PARAMETER
Content-Type: application/sdp
Content-Length: 177
v=0
o=- 173050 0 IN IP4 62.65.253.102
s=RTSP Session
t=0 0
c=IN IP4 62.65.253.102
b=AS:8586.000
a=type:vod
a=range:npt=0-139
m=video 0 UDP 33
m=video 0 RTP/AVP/UDP 33

'''

responseTeardown = '''
RTSP/1.0 200 OK
CSeq: %s
Session: %s
Date: %s
Server: Broadbus RTSP Server
Range: npt=3440-

'''

responseSessionCount = '''
RTSP/1.0 200 OK
CSeq: %s
Date: %s
Content-Type: text/parameters
Server: Broadbus RTSP Server
Content-Length: %s

session_count: %s

'''

responseSessionList = '''
RTSP/1.0 200 OK
CSeq: %s
Date: %s
Content-Type: text/parameters
Server: Broadbus RTSP Server
Content-Length: %s

session_list: %s

'''

def curdatetime():
	return time.strftime("%a, %d %b %Y %H:%M:%S GMT", time.gmtime())

def handler(clientsock,clientaddr):
	while True:
		#Receive data from connected client socket
		data = clientsock.recv(1024)
		#print data
		if data:
			print '=== received request ==='
			print data
			print ''
			#Find out the CSEQ no of the REQUEST and use in response
			patternCSEQ = re.compile(r'CSeq: (\d+)', re.MULTILINE)
			seqNo = re.findall(patternCSEQ, data)[0]
			
			#Find out which RTSP Request is sent
			patternRTSP = re.compile(r'.*RTSP/1.0.*', re.MULTILINE)
			rtspRequest = re.findall(patternRTSP, data)
			rtspRequestBody = data.split('\r\n\r\n')[1]
			
			#SET RTSP Response based on RTSP Request
			if re.findall(re.compile(r'.*SETUP.*', re.MULTILINE), rtspRequest[0]) != []:
				print 'Received: SETUP'
				sessionid = randrange(1000000000000000,9999999999999999)
				i = 0
				while os.path.exists(sessionDb + str(sessionid)) == True:
					if i == 1000:
						print 'Tried', i, 'times to create a new session id, but I can\'t find one :('
						sessionid = 'krak'
						break
					print sessionid, 'exists, creating new random id'
					sessionid = randrange(1,9)
					i += 1
				if sessionid != 'krak':
					f = open(sessionDb + str(sessionid), 'w')
					f.close()
					rtspResponse = responseSetup % (seqNo, sessionid, curdatetime())
				else:
					rtspResponse = responseInternalServerError % seqNo
			
			elif re.findall(re.compile(r'.*PLAY.*', re.MULTILINE), rtspRequest[0]) != []:
				print 'Received: PLAY'
				patternSession = re.compile(r'Session: (\d+)', re.MULTILINE)
				sessionId = re.findall(patternSession, data)[0]
				
				if os.path.exists(sessionDb + '\\' + str(sessionId)):
					rtspResponse = responseOk % (seqNo, curdatetime())
				else:
					rtspResponse = responseSessionNotFound % (seqNo, sessionId, curdatetime())
			
			elif re.findall(re.compile(r'.*GET_PARAMETER.*', re.MULTILINE), rtspRequest[0]) != []:
				if rtspRequestBody.startswith('session_count'):
					print 'Received: SESSION_COUNT'
					
					currentsessionscount = len([file for root,dirs,files in os.walk(sessionDb) for file in files])
					bodylength = str(len("session_count: " + str(currentsessionscount)))
					
					rtspResponse = responseSessionCount % (seqNo, curdatetime(), bodylength, str(currentsessionscount))
				elif rtspRequestBody.startswith('session_list'):
					print 'Received: SESSION_LIST'
					
					currentsessions = [file for root,dirs,files in os.walk(sessionDb) for file in files]
					bodylength = str(len('session_list: ' + ' '.join(currentsessions)))
					
					rtspResponse = responseSessionList % (seqNo, curdatetime(), bodylength, ' '.join(currentsessions))
				else:
					print 'Received: GET_PARAMETER'
					
					rtspResponse = responseOk % (seqNo, curdatetime())
			
			elif re.findall(re.compile(r'.*DESCRIBE.*190/ RTSP/1.0$', re.MULTILINE), rtspRequest[0]) != []:
				print 'Received: DESCRIBE ERROR'
				rtspResponse = responseBadRequest % (seqNo, curdatetime())
			
			elif re.findall(re.compile(r'.*DESCRIBE.*', re.MULTILINE), rtspRequest[0]) != []:
				print 'Received: DESCRIBE'
				rtspResponse = responseDescribe % (seqNo, curdatetime())
			
			elif re.findall(re.compile(r'.*TEARDOWN.*', re.MULTILINE), rtspRequest[0]) != []:
				print 'Received: TEARDOWN'
				
				patternSession = re.compile(r'Session: (\d+)', re.MULTILINE)
				sessionId = re.findall(patternSession, data)[0]
				
				if os.path.exists(sessionDb + '\\' + str(sessionId)):
					try:
						os.remove(sessionDb + '\\' + str(sessionId))
						rtspResponse = responseTeardown % (seqNo, sessionId, curdatetime())
					except:
						rtspResponse = responseInternalServerError % seqNo
				else:
					rtspResponse = responseSessionNotFound % (seqNo, sessionId, curdatetime())
				
				
			#Send the appropriate rtspResponse back
			print '=== sent request ==='
			print rtspResponse
			clientsock.send(rtspResponse) 
		else:
			break
		
	#Close socket
	clientsock.close()

if __name__=='__main__':
	#Initialize server socket  with appropriate modes
	s = socket(AF_INET, SOCK_STREAM)
	s.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
	
	#Bind server to a IP/Port tuple and allow multiple connects
	s.bind((args.listen_address, args.listen_port))
	s.listen(5)
	
	#Set up continuous loop to listen for connections and print connected ip's
	while True:
		print 'waiting for connection...'
		clientsock, clientaddr = s.accept()
		print '...connected from:', clientaddr
		
		#Start new thread per connected client socket
		thread.start_new_thread(handler, (clientsock, clientaddr))