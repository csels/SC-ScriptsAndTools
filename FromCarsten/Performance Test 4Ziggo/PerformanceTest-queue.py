'''
Created on Jan 4, 2013

@author: csels
'''
import threading
import os
import Queue
import time
import re

path = r'C:\VODUsageFiles1'
files = os.listdir(path)
print len(files)
queue = Queue.Queue()
threads = []

class MyThread(threading.Thread):
    def __init__(self, queue, threadNumber):
        threading.Thread.__init__(self)
        self.queue = queue
        self.threadNumber = threadNumber
        self.lines = []
        
    def run(self):
        while True:
            #Grab file from queue
            file = self.queue.get()
            f = open(file)
            #firstLine
            i=0
            for line in f:
                if i==0:
                    self.lines.append(line.rstrip())
                    print '%i. %s' % (self.threadNumber,line.rstrip())
                i+=1
            self.queue.task_done()

start = time.time()
def main():
    #Create 5 threads and pass them the queue instance
    for i in range(5):
        t = MyThread(queue, i)
        t.setDaemon(True)
        t.start()
        threads.append(t)
    
    #Create queue with urls for each STB and process it
    for stb in range(2):
        for url in range(2):
            print urls[url]
            queue.put(urls[url])
            
        
    for (paths, dirs, files) in os.walk(path):
        for fi in files:
            print fi
            pattern = re.compile('Transactions')
            if re.search(pattern, fi) is not None:
                queue.put(os.path.join(paths,fi))
    
    #Wait till all files in queue are processed    
    queue.join()
    
    for t in threads:
        print 'Thread %i' % t.threadNumber
        for line in t.lines:
            print '\t', line
        print
    
main()      
print "Elapsed Time: %s" % (time.time() - start)
 