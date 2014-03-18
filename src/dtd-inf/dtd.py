#!/usr/local/bin/python3

import argparse
import itertools
import os.path
import sys
import time
import xml.etree.cElementTree as ET
import modod

from modod.soa import SingleOccurrenceAutomaton


parser = argparse.ArgumentParser(description="This tool takes a list of XML files and computes a DTD.",epilog="Default is inferring an element type definition for every element in the files. If you want to compute this for only some elements, use the -e flag. If you want to exclude elements that have empty definitions, use the -s flag. See the readme file for hidden arguments.")
parser.add_argument("files",help="the XML file(s) from which the element type declarations are to be inferred",nargs="+")

parser.add_argument("-a","--automaton",help=argparse.SUPPRESS,dest="autprefix",type=str,nargs="?",default="")
parser.add_argument("-c","--chare",help="infer a chain regular expression, instead of a single occurrence regular expression (the former are flatter than the latter)",action="store_true")
parser.add_argument("-co","--counts",help=argparse.SUPPRESS,dest="counts",action="store_true")
parser.add_argument("-d","--dre",help="write output as deterministic regular expression, instead of an element type declaration (also activates -j)",action="store_true")
parser.add_argument("-e","--elements",help="determines for which element names an element type declaration is inferred",dest="elements",nargs="+",default=[])
parser.add_argument("-j","--just-elements",help="do not put the DOCTYPE declaration around the element tags",dest="justelements",action="store_true")
parser.add_argument("-n","--no-inference",help=argparse.SUPPRESS,dest="noinference",action="store_true")
parser.add_argument("-s","--skip-empty",help="do not display declarations of elements that have no childer",dest="skipempty",action="store_true")
parser.add_argument("-t","--timestamps",help=argparse.SUPPRESS,action="store_true")
parser.add_argument("-u","--ugly",help="do not use prettification algorithm",action="store_true")
parser.add_argument("-v","--verbose",help=argparse.SUPPRESS,dest="verbose",action="store_true")
parser.add_argument("-we","--write-elements",help=argparse.SUPPRESS,action="store_true",dest="writeElements")
parser.add_argument("-wep","--write-prefix",help=argparse.SUPPRESS,action="store_true",dest="writeprefix",default="")
parser.add_argument("-wes","--write-suffix",help=argparse.SUPPRESS,action="store_true",dest="writesuffix",default=".dtd")

#parser.add_argument("-a","--automaton",help="for every element E, the inferred SOA is written to the file AUTPREFIX E.dot in the dot-format of Graphviz",dest="autprefix",type=str,nargs="?",default="")
#parser.add_argument("-co","--counts",help="display how often elements occur",dest="counts",action="store_true")
#parser.add_argument("-n","--no-inference",help="do not infer element type declarations (only useful if -a is used as well)",dest="noinference",action="store_true")
#parser.add_argument("-t","--timestamps",help="includes some timestamps (for very elementary profiling) ",action="store_true")
#parser.add_argument("-v","--verbose",help="print additional information",dest="verbose",action="store_true")
#parser.add_argument("-we","--write-elements",help="for every element E, write the inferred DTD/regular expression to a file WPREFIX E.WSUFFIX (definable by -wp,-ws)",action="store_true",dest="writeElements")
#parser.add_argument("-wep","--write-prefix",help="sets WPREFIXe (for -we), default empty",action="store_true",dest="writeprefix",default="")
#parser.add_argument("-wes","--write-suffix",help="sets WPREFIXe (for -we), default .dtd",action="store_true",dest="writesuffix",default=".dtd")


#parser.add_argument("-f","--force",help="necessary if no list of elements is provided",action="store_true")


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
		p = modod.DREfromString(regex).toNNF().toString()
		return p.replace('+?','*')
	else: 
		return ''
allElts=False
elementnames = args.elements
filenames = args.files
skipempty = args.skipempty
timestamps = args.timestamps
ugly=args.ugly
verbose = args.verbose
writeprefix = args.writeprefix
writesuffix = args.writesuffix
writeWrapper = ((not args.justelements) and (not args.dre)) # if we do not write the DOCTYPE stuff, DREs make no sense.	

startTime = time.time()

if (elementnames==[]):
	allElts=True

for f in filenames:
	if not os.path.isfile(f):
		sys.stderr.write("***ERROR***\nFile "+f+" not found.\n")
		sys.exit()	

# generate the SOAs
soas = {}
scount = {}

rootName = ''

for fn in filenames:
	tmessage('Parsing XML file'+fn)
	root = ET.parse(fn)
	if writeWrapper:
		if (rootName == ''):
			rootName=root.getroot().tag
		elif (rootName!=root.getroot().tag):
			sys.exit('Root names in XML documents do not match. If this does not matter to you, use the -j flag.')
	
	tmessage('Starting iterating the tree')
	for found in root.iter():
		if (found.tag in elementnames) or allElts:
			if found.tag not in soas:
				soas[found.tag] = SingleOccurrenceAutomaton()
				scount[found.tag] = 0
				
			word = [SingleOccurrenceAutomaton.src]
			for child in found:
				word = word + [child.tag]
			word = word + [SingleOccurrenceAutomaton.snk]
			soas[found.tag].addWord(word)
			scount[found.tag] = scount[found.tag] + 1
			message("Added "+str(word)+" to "+str(found.tag))

tmessage('Finished XML processing')
	
		
for elt in soas:
	if elt not in soas:
		soas[elt] = SingleOccurrenceAutomaton()
		scount[elt] = 0
	if args.counts:
		print(elt, scount[elt])

# process the SOAs		
sores = {}
for elt in soas:
	if args.noinference:
		sys.exit('You chose not to infer, so we are done.')

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
	
	if not ugly:
		sore=pretty(sore)

	if (sore == '') and skipempty:
		continue
	
	if sore[-1:]!=')':
		sore = '('+sore+')'

	if (not args.dre):
		sore = '<!ELEMENT '+elt+' '+sore+'>'

	sores[elt]=sore

if writeWrapper:
	print('<!DOCTYPE ['+rootName)
	# preferential treatment of the root element, looks nicer
	print(sores[rootName])
	if args.writeElements:
		fn = writeprefix+rootName+writesuffix
		soreFile = open(fn,'w')
		soreFile.write(sores[rootName])
		soreFile.close()
		message(elt+" written to file.")
	del sores[rootName]

for elt in sores:
	print(sores[elt])
	if args.writeElements:
		fn = writeprefix+elt+writesuffix
		soreFile = open(fn,'w')
		soreFile.write(sores[elt])
		soreFile.close()
		message(elt+" written to file.")

if writeWrapper:
	print(']>')

tmessage('Done.')
