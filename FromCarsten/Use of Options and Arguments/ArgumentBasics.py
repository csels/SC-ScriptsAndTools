'''
Created on Aug 28, 2013

@author: csels

NOTE: This script is only usable starting from Python interpreter 2.7 (NO 2.6!!!!)
'''
import optparse

#Instantiate parser
parser = optparse.OptionParser("usage: %prog [options] arg1 arg2")

#Add parser options
parser.add_option('-v', '--verbose', dest='verbose', help='This switch enables the verbose mode of the script.', default=True)
parser.add_option('-f', '--file', dest='file', help='Define the output file.', default=True)

#Instruct the parser to parse the options and arguments
(options, args) = parser.parse_args()
    
verbose=options.verbose
filen=options.file

print verbose
print filen