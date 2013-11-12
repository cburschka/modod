import xml.etree.cElementTree as ET
import time

from soa import SingleOccurrenceAutomaton

chatty = False
# chatty = True # set to True if you want timestamps etc

def timeStamp():
	return round((time.time() - startTime),3)

def message(m):
	if chatty:
		print(timeStamp(), m)

filenames=['mondial.xml']
elementnames=['country']#,'province','city','organization','source','estuary','river','lake','sea','desert','island','mountain','mondial','geo']

chareFile = open('chares.txt','w')
chareFile.write('')
chareFile.close()

soreFile = open('sores.txt','w')
soreFile.write('')
soreFile.close()

startTime = time.time()
wordcounter = 0
for elt in elementnames:
	#print "Inferring Element "+str(elt)
	message("Inferring Element "+elt)
	soa = SingleOccurrenceAutomaton()
	for fn in filenames:
		#rint(timeStamp(), "Parsing XML file",fn)
		root = ET.parse(fn)
		message("Parsed")
		message("Searching tree")
		for found in root.findall('.//'+elt): # this is highly inefficient, but still kinda okay
			word = [SingleOccurrenceAutomaton.src]
			for child in found:
				word = word + [child.tag]
			word = word + [SingleOccurrenceAutomaton.snk]
	#print("adding ",word)
			soa.addWord(word)
			wordcounter += 1
	message("SOA created") 
	soaFile= open('soa'+elt+'.dot', 'w')
	soaFile.write(soa.toDotString())
	soaFile.close()
	if soa.succ=={}:
		chare = ''
	else:
		chare=soa.chare()

	elem = '<!ELEMENT '+elt+' ('+chare+')>'
	message('CHARE:')
	print(elem)
	#print "CHARE: "+elem
	chareDTDFile = open('dtd-chares.txt','a')
	chareDTDFile.write(elem)
	chareDTDFile.write('\n')
	chareDTDFile.close()
	if soa.succ=={}:
		sore = ''
	else:
		sore=soa.sore()
	elem = '<!ELEMENT '+elt+' ('+sore+')>'
	message('SORE:')
	print(elem)
	#print "SORE: "+elem
	soreDTDFile = open('dtd-sores.txt','a')
	soreDTDFile.write(elem)
	soreDTDFile.write('\n')
	soreDRDFile.close()
	message('Number of processed elements: '+str(wordcounter))
