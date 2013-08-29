'''
Created on May 16, 2013

@author: csels
'''
import re
import datetime
import os

traxisLogsDirectory = r'C:\Users\csels\workspace\SeaChange scripts\src\TraceRTSP\Traxis Logs'
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
        regexRtspOrbitError = re.compile('.*\[RequestId = (.*?)\].*\n.*(RTSP/1.0 [3-9][0-9]+?.*)', re.M|re.I)   
        requestToRTSPErrorMappings = re.findall(regexRtspOrbitError, text)
        
        #Count all unique RTSP Errors
        uniqueRTSPErrors={}
        uniqueSetups={}
        for r in requestToRTSPErrorMappings:
            if r[1] != 'RTSP/1.0 451 Parameter Not Understood':
                if r[1] not in uniqueRTSPErrors:
                    uniqueRTSPErrors[r[1]] = 1
                    uniqueSetups[r[1]] = []
                    uniqueSetups[r[1]].append(r[0])
                else:
                    uniqueRTSPErrors[r[1]] += 1
                    uniqueSetups[r[1]].append(r[0])
        
        #Print unique RTSP Errors with their count
        for k,v in uniqueRTSPErrors.iteritems():
            print 'Error %s \t\t[found %sx in provided logs]' % (k,v)
            
        for k,v in uniqueSetups.iteritems():
            for request in v:
                regexRtspSetupForRequestId = re.compile('(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}).*\[RequestId = %s\].*\n.*(SETUP.*RTSP/1.0.*)' % request, re.M|re.I) 
                rtspSetupsForRequestId = re.findall(regexRtspSetupForRequestId, text)
                
                print '[%s]' % k
                print 'Corresponding SETUPS:'
                for rtspSetupForRequestId in rtspSetupsForRequestId:
                    print '\t(%s) %s' % (rtspSetupForRequestId[0], rtspSetupForRequestId[1])
                    
        print 'Analysis ended at %s' % datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        print '\n'