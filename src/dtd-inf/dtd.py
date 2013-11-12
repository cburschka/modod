#!/usr/local/bin/python3

import argparse
import xml.etree.cElementTree as ET
from soa import SingleOccurrenceAutomaton
import os.path
import sys

parser = argparse.ArgumentParser(description="TODO: What this tool does",epilog="TODO: Further info")
parser.add_argument("files",help="the XML file(s) from which the element type declarations are to be inferred",nargs="+")

parser.add_argument("-a","--automaton",help="for every element E, the inferred SOA is written to the file AUTPREFIX E.dot in the dot-format of Graphviz",dest="autprefix",type=str,nargs="?",default="")
parser.add_argument("-c","--chare",help="infer a chain regular expression, instead of a single occurrence regular expression",action="store_true")
parser.add_argument("-d","--dre",help="write output as deterministic regular expression, instead of an element type declaration",action="store_true")
parser.add_argument("-e","--elements",help="determines for which element names an element type declaration is inferred",dest="elements",nargs="+",default=[])
parser.add_argument("-f","--force",help="necessary if no list of elements is provided",action="store_true")
parser.add_argument("-n","--no-inference",help="do not infer element type declarations (only useful if -a is used as well)",dest="noinference",action="store_true")
parser.add_argument("-v","--verbose",help="print additional information and time stamps",dest="verbose",action="store_true")
parser.add_argument("-w","--write",help="for every element E, write the inferred DTD/regular expression to a file WPREFIX E.WSUFFIX (definable by -wp,-ws)",action="store_true",dest="writeToFile")
parser.add_argument("-wp","--write-prefix",help="sets WPREFIXe (for -w)",action="store_true",dest="writeprefix",default="")
parser.add_argument("-ws","--write-suffix",help="sets WPREFIXe (for -w)",action="store_true",dest="writesuffix",default="dtd")

args=parser.parse_args()

def timeStamp():
	return round((time.time() - startTime),3)

def message(m):
	if args.verbose:
		print(timeStamp(), m)

filenames = args.files
elementnames = args.elements

if (elementnames==[]):
	if not args.force:
		sys.stderr.write("***ERROR***\nNo list of elements provided. Default behaviour is to infer an element type definition for every element in the file or list of files. This is probably very, very slow. If you really want to do this, use the -f option. (As soon as this function is implemented.)\n")
	else:
		sys.stderr.write("***ERROR***\nNo list of elements provided. Not yet implemented.\n")
for f in filenames:
	if not os.path.isfile(f):
		sys.stderr.write("***ERROR***\nFile "+f+" not found.\n")
		sys.exit()	


for elt in elementnames:
	message("Inferring Element "+elt)
	soa = SingleOccurrenceAutomaton()
	for fn in filenames:
		message('Parsing XML file '+fn)
		root = ET.parse(fn)
		message("Parsed. Searching tree")
		for found in root.findall('.//'+elt): # this is highly inefficient, but still kinda okay
			word = [SingleOccurrenceAutomaton.src]
			for child in found:
				word = word + [child.tag]
			word = word + [SingleOccurrenceAutomaton.snk]
			soa.addWord(word)
	message("SOA for "+elt+" created") 
	
	if (args.autprefix != ''):
		if args.autprefix==None:
			autpref = 'SOA-'
		else:
			autpref = args.autprefix
		soaFile= open(autpref+elt+'.dot', 'w')
		soaFile.write(soa.toDotString())
		soaFile.close()
		
	if args.noinference:
		print("You chose no inference, so that's all.")
		sys.exit()
		
	if args.chare:
		sore = soa.chare()
	else:
		sore = soa.sore()
	
	# Normalform nach hier:
	sore = '('+sore+')'

	if not args.dre:
		sore = '<!ELEMENT '+elt+' '+sore+'>'

	print(sore)
	
	if args.writeToFile:
		fn = writeprefix+elt+writesuffix
		soreFile = open(fn,'w')
		soreFile.write(sore)
		soreFile.close()
		message(elt+" written to file.")
