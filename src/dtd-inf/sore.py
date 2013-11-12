#!/usr/local/bin/python3
import argparse
from soa import SingleOccurrenceAutomaton 

parser = argparse.ArgumentParser(description="This tool reads a finite sample and computes an appropriate descriptive SOA, and SORE or CHARE",epilog="Sample use: sore.py -c ab abd cde ce")

parser.add_argument("words",help="the words of the sample",nargs="+")

parser.add_argument("-a","--automaton",help="for every element E, the inferred SOA is written to the file AUTOMATON in the dot-format of Graphviz",dest="soafilename")
parser.add_argument("-c","--chare",help="infer a chain regular expression (CHARE), instead of a single occurrence regular expression (SORE)",action="store_true")
parser.add_argument("-o","--outfile",help="write result to OUTFILE",dest="outfilename")

args=parser.parse_args()
			
soa = SingleOccurrenceAutomaton()

for w in args.words:
	soa.addString(w)

if args.soafilename!=None: 
	soaFile= open(args.soafilename, 'w')
	soaFile.write(soa.toDotString())
	soaFile.close()

if args.chare:
	sore = soa.chare()
else:
	sore = soa.sore()

print(sore)

if args.outfilename!=None:
	soreFile = open(args.outfilename)
	soreFile.write(sore)
	soreFile.close()


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

	