#!/usr/local/bin/python3

import argparse
import itertools
import os.path
import sys
import time
import xml.etree.cElementTree as ET
import modod

from soa import SingleOccurrenceAutomaton


parser = argparse.ArgumentParser(description="TODO: What this tool does",epilog="TODO: Further info")
parser.add_argument("files",help="the XML file(s) from which the element type declarations are to be inferred",nargs="+")

parser.add_argument("-a","--automaton",help="for every element E, the inferred SOA is written to the file AUTPREFIX E.dot in the dot-format of Graphviz",dest="autprefix",type=str,nargs="?",default="")
parser.add_argument("-c","--chare",help="infer a chain regular expression, instead of a single occurrence regular expression",action="store_true")
parser.add_argument("-d","--dre",help="write output as deterministic regular expression, instead of an element type declaration",action="store_true")
parser.add_argument("-e","--elements",help="determines for which element names an element type declaration is inferred",dest="elements",nargs="+",default=[])
parser.add_argument("-f","--force",help="necessary if no list of elements is provided",action="store_true")
parser.add_argument("-n","--no-inference",help="do not infer element type declarations (only useful if -a is used as well)",dest="noinference",action="store_true")
parser.add_argument("-s","--skip-empty",help="do not display declarations of elements that have no childer",dest="skipempty",action="store_true")
parser.add_argument("-t","--timestamps",help=argparse.SUPPRESS,action="store_true")
parser.add_argument("-v","--verbose",help=argparse.SUPPRESS,dest="verbose",action="store_true")
# parser.add_argument("-t","--timestamps",help="show timestamps for important tasks",action="store_true")
# parser.add_argument("-v","--verbose",help="print additional information and time stamps",dest="verbose",action="store_true")
parser.add_argument("-we","--write-elements",help="for every element E, write the inferred DTD/regular expression to a file WPREFIX E.WSUFFIX (definable by -wp,-ws)",action="store_true",dest="writeElements")
parser.add_argument("-wep","--write-prefix",help="sets WPREFIXe (for -w), default empty",action="store_true",dest="writeprefix",default="")
parser.add_argument("-wes","--write-suffix",help="sets WPREFIXe (for -w), default .dtd",action="store_true",dest="writesuffix",default=".dtd")

args=parser.parse_args()

def timeStamp():
	return round((time.time() - startTime),3)

def tmessage(m):
	if timestamps:
		print(timeStamp(), m)

def message(m):
	if verbose:
		print(timeStamp(), m)

def pretty(regex):
	# Test:
	message('Prettifying '+regex)
	if regex != '':
		p = modod.write(modod.nnf(modod.parse(regex)))
		return p.replace('+?','*')
	else: 
		return ''

allElts = args.force
elementnames = args.elements
filenames = args.files
skipempty = args.skipempty
timestamps = args.timestamps
verbose = args.verbose
writeprefix = args.writeprefix
writesuffix = args.writesuffix

startTime = time.time()

if (elementnames==[]):
	if not args.force:
		sys.stderr.write("***ERROR***\nNo list of elements provided. Default behaviour is to infer an element type definition for every element in the file or list of files. This is probably very, very slow. If you really want to do this, use the -f option. (As soon as this function is implemented.)\n")

for f in filenames:
	if not os.path.isfile(f):
		sys.stderr.write("***ERROR***\nFile "+f+" not found.\n")
		sys.exit()	


# generate the SOAs
soas = {}

for fn in filenames:
	tmessage('Parsing XML file'+fn)
	root = ET.parse(fn)
	tmessage('Starting iterating the tree')
	for found in root.iter():
#	for found in itertools.chain(root.findall('.'),root.findall('.//*')):
		if (found.tag in elementnames) or allElts:
			if found.tag not in soas:
				soas[found.tag] = SingleOccurrenceAutomaton()
				
			word = [SingleOccurrenceAutomaton.src]
			for child in found:
				word = word + [child.tag]
			word = word + [SingleOccurrenceAutomaton.snk]
			soas[found.tag].addWord(word)
			message("Added "+str(word)+" to "+str(found.tag))
	tmessage('Done with iterating the tree')
	
		
for elt in soas:
	if elt not in soas:
		soas[elt] = SingleOccurrenceAutomaton()

# process the SOAs		
for elt in soas:
	if args.noinference:
		print("You chose not to infer, so that's all.")
		sys.exit()

	tmessage('Processing soa of '+str(elt))
	if (args.autprefix != ''):
		if args.autprefix==None:
			autpref = 'SOA-'
		else:
			autpref = args.autprefix
		soaFile= open(autpref+elt+'.dot', 'w')
		soaFile.write(soas[elt].toDotString())
		soaFile.close()
				
	if args.chare:
		sore = soas[elt].chare()
	else:
		sore = soas[elt].sore()

	sore=pretty(sore)

	if (sore == '') and skipempty:
		continue
	
	# Normalform nach hier:
	sore = '('+sore+')'

	if not args.dre:
		sore = '<!ELEMENT '+elt+' '+sore+'>'

	print(sore)
	
	if args.writeElements:
		fn = writeprefix+elt+writesuffix
		soreFile = open(fn,'w')
		soreFile.write(sore)
		soreFile.close()
		message(elt+" written to file.")
