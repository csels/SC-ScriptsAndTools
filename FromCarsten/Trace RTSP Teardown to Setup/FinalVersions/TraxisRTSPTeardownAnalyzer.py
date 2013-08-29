'''
Created on May 16, 2013

@author: csels
'''
import re
import datetime
import os

traxisLogsDirectory = r'C:\Users\csels\workspace\SeaChange scripts\src\TraceRTSP\Traxis Logs\FE1'
for traxisLog in os.listdir(traxisLogsDirectory):
    #Only parse RTSPTraxisLogs using the regex
    pattern = re.compile(r'RtspTraxisService.log.*')
    if re.search(pattern, os.path.join(traxisLogsDirectory, traxisLog)) is not None:
        print 'Current file: %s' % traxisLog
        print 'Analysis started at %s' % datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        f = open(os.path.join(traxisLogsDirectory, traxisLog), 'r')
        with open(os.path.join(traxisLogsDirectory, traxisLog), "r") as fobj:
            text = fobj.read()
        
        #Find all request ID's for all RTSP Errors from Orbit or sent back to STB
        #Save Request ID (of teardown)([0]), Session ID ([1]) and Teardown Reason ([3])  
        regexRtspTeardownError = re.compile('(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}).*\[RequestId = (.*)\].*\nTEARDOWN.*\n.*\nSession: (.*)\n(Reason: .*)', re.M|re.I)   
        requestToRTSPTeardownMappings = re.findall(regexRtspTeardownError, text)
        
        #Count all unique RTSP Errors
        #Save all unique Session IDs for every RTSP Teardown Reason
        uniqueRTSPTeardownReasons={}
        uniquePRSessions={}
        for r in requestToRTSPTeardownMappings:
            if r[3] not in uniqueRTSPTeardownReasons:
                uniqueRTSPTeardownReasons[r[3]] = 1
                uniquePRSessions[r[3]] = []
                uniquePRSessions[r[3]].append(r[2])
            else:
                uniqueRTSPTeardownReasons[r[3]] += 1
                uniquePRSessions[r[3]].append((r[0], r[2]))
        
        #Print dictionary: show the unique RTSP Teardown Reasons along with their count
        totalRTSPTeardownOccurrences = 0
        for k,v in uniqueRTSPTeardownReasons.iteritems():
            print 'RTSP Teardown %s \t\t[found %sx in provided logs]' % (k,v)
            totalRTSPTeardownOccurrences += v
        
        #Go through each session array in the dictionary for every RTSP Teardown reason    
        for k,v in uniquePRSessions.iteritems():
            print k,v
            if k != 'Reason: 200 User Pressed Stop' or k!= 'Reason: 201 End of Stream':
                for PRSession in v:
                    #Find the RTSP OK sent to STB for that Session ID
                    #Correlate the Request ID for the RTSP Setup from this RTSP OK (Other than the RTSP Teardown request iD
                    regexRtspResponsesOK = re.compile('(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}).*\[RequestId = (.*?)\].*Message send to.*:\n(RTSP/1.0 200 OK\n.*\nSession: %s.*\n.*\nControlSession: .*\n.*\n.*\n.*\n.*\n.*)' % PRSession[1], re.MULTILINE) 
                    okRequestIDs = re.findall(regexRtspResponsesOK, text)
                    
                    #Go through the array of OKRequestIDs tuples(okReply[0], okRrequestID[1])
                    for okRequestID in okRequestIDs:
                        #Find the RTSP Setup based on the Request ID in the OK Reply sent back to STB
                        regexRtspSetup = re.compile('(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}).*\[RequestId = %s\].*\n.*(SETUP.*STBID.*RTSP/1.0.*)' % okRequestID[1], re.M|re.I) 
                        rtspSetups = re.findall(regexRtspSetup, text)
                        
                        #Finally print the unique RTSP Teardown Reason, corresponding RTSP Setup, and corresponding RTSP OK Reply to STB
                        for rtspSetup in rtspSetups:    
                            print '[(%s) RTSP Teardown %s]\n(%s) %s\n(%s) %s' % (PRSession[0], k, rtspSetup[0], rtspSetup[1], okRequestID[0], okRequestID[2].replace('\n', '\n\t'))
        
        #Analysis ended timestamp            
        print 'Analysis ended at %s' % datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        print '\n'