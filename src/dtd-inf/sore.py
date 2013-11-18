#!/usr/local/bin/python3
import argparse
from soa import SingleOccurrenceAutomaton 
import modod

def pretty(regex):
	# Test:
	if regex != '':
		p = modod.DREfromString(regex).toNNF().toString()
		return p.replace('+?','*')
	else: 
		return '()'

parser = argparse.ArgumentParser(description="This tool reads a finite list of words and computes an appropriate descriptive SOA, and SORE or CHARE. ",epilog="Sample use: sore.py -c ab abd cde ce")

parser.add_argument("words",help="the words of the sample",nargs="+")

parser.add_argument("-a","--automaton",help="for every element E, the inferred SOA is written to the file AUTOMATON in the dot-format of Graphviz",dest="soafilename")
parser.add_argument("-c","--chare",help="infer a chain regular expression (CHARE), instead of a full SORE",action="store_true")
parser.add_argument("-o","--outfile",help="write result to OUTFILE",dest="outfilename")
parser.add_argument("-s","--space",help="use space as concatenation symbol (instead of comma)",action="store_true")
parser.add_argument("-u","--ugly",help="do not use prettification algorithm",action="store_true")

args=parser.parse_args()

chare=args.chare
outfilename=args.outfilename
soafilename=args.soafilename
space=args.space
ugly=args.ugly
words=args.words

soa = SingleOccurrenceAutomaton()

for w in words:
	soa.addString(w)

if soafilename!=None: 
	soaFile= open(soafilename, 'w')
	soaFile.write(soa.toDotString())
	soaFile.close()

if chare:
	sore = soa.chare()
else:
	sore = soa.sore()

if not ugly:
	sore=pretty(sore)

if space:
	sore=sore.replace(',',' ')

if outfilename!=None:
	soreFile = open(outfilename)
	soreFile.write(sore)
	soreFile.close()
else:
	print(sore)
	
# begin ping lu
# soa.addString("ababc")
# soa.addString("abcdabc")
# soa.addString("dabcjcfhafdej")
# soa.addString("egghifg")
# soa.addString("i")
# end ping lu

#soa.addString("ababcbc")

# soa.addString("ab")
# soa.addString("abd")
# soa.addString("cde")
# soa.addString("ce")

	