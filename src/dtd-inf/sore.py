from soa import SingleOccurrenceAutomaton 
			
soa = SingleOccurrenceAutomaton()
# begin ping lu
# soa.addString("ababc")
# soa.addString("abcdabc")
# soa.addString("dabcjcfhafdej")
# soa.addString("egghifg")
# soa.addString("i")
# end ping lu

soa.addString("ababcbc")

# soa.addString("ab")
# soa.addString("abd")
# soa.addString("cde")
# soa.addString("ce")
	
print(soa.sore())

	