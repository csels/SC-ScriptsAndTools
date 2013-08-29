'''
Created on Feb 25, 2013

@author: csels
'''
import zipfile, tarfile
import os, datetime

#Define variables
toZipPath = r'C:\Users\csels\workspace\SeaChange scripts\src\UntarAndZip\mixed tape'
tarPath = r'C:\Users\csels\workspace\SeaChange scripts\src\UntarAndZip\testtars'
extractedPath = r'C:\Users\csels\workspace\SeaChange scripts\src\UntarAndZip\Extracted'
treshold = 8192

if not os.path.exists(extractedPath):
    os.mkdir(extractedPath)

#Set the ZipStartTime
timeStarted = datetime.datetime.now()
timeStarted = timeStarted.strftime("%Y-%m-%d %H:%M:%S")
print 'Compression to ZIP started at %s' % timeStarted

#Extract TAR files
for tar in os.listdir(tarPath):
    if tar[-4:] == '.tar':
        print tar
        tarSize = os.path.getsize(os.path.join(tarPath, tar))
        
        #Tar size is smaller than 8GB so just move to normal ingest folder
        if (tarSize / (1024*1024)) < treshold:
            #Insert logic for moving TAR file to normal ingest folder
            print 'Moving logic normal files.'
        
        #Tar size is larger than 8GB so first extract the contents of it
        elif (tarSize / (1024*1024)) > (treshold-1):
            tarFile = tarfile.open(os.path.join(tarPath, tar), 'r')
            #Extract every file in Tar to Extracted Path
            for item in tarFile:
                tarFile.extract(item, extractedPath)
                print 'Extracted %s succesfully to %s' % (item.name, extractedPath)
            
            #Change to the directory to ExtractedPath so all of the files in there can be zipped
            os.chdir(extractedPath)
            
            #Create a new ZIP file for the contents
            zipName = '%s.zip' % tar[:-4]
            print zipName
            myZipFile = zipfile.ZipFile(zipName, 'w', allowZip64=True)
            
            #Add all extracted files to the new ZIP but exclude the ZIP file itself
            for f in os.listdir('.'):
                if f[-4:] != '.zip':
                    myZipFile.write(f)
                    print 'Sucessfully added %s to %s.' % (f,zipName)
            
            # flush and close the create ZIP buffer
            myZipFile.close()

#Set the ZipEndTime    
timeEnded = datetime.datetime.now()
timeEnded = timeEnded.strftime("%Y-%m-%d %H:%M:%S")    
print 'Compression to ZIP ended at %s' % timeEnded
