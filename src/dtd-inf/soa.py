#!/usr/bin/python
# -*- coding: iso-8859-15 -*-

import xml.etree.cElementTree as ET
import time

#dbmode = True # set to True for excessive print Debugging
dbmode = False

class SingleOccurrenceAutomaton:
	"""A class for single occurrence automata (SOA)"""
	src = 0
	snk = 1
	def __init__(self):
		self.succ = {}
		self.epscount = 0

	def setEdges(self,edgeblob):
		self.succ = edgeblob
	
	def nodeList(self):
		#returns a list of all nodes of the SOA
		# assumes that soa is strongly connected, snk always reachable
		nl = []
		for s in self.succ:
			nl += [s]
		nl += [SingleOccurrenceAutomaton.snk]
		return nl
	
	def addString(self,string):
		w = [SingleOccurrenceAutomaton.src]
		for a in string:
			w += [a]
		w += [SingleOccurrenceAutomaton.snk]
		self.addWord(w)
	
	def addWord(self,word):
		for i in range(0,len(word)-1):
			if word[i] not in self.succ:
				self.succ[word[i]] = [word[i+1]]
			elif word[i+1] not in self.succ[word[i]]:
				self.succ[word[i]] = self.succ[word[i]]+[word[i+1]]
	
	def toDotString(self):
		dotString = 'digraph untitled {\n'
		for node in self.succ:
			dotString += self.dotNodeString(node)
		dotString += self.dotNodeString(self.snk)
		for node in self.succ:
			for t in self.succ[node]:
				dotString += str(self.identifier(node))+'->'+self.identifier(t)+';\n'
		dotString += '}'
		return dotString
	
	def contractSCLC(self):
		nl = self.nodeList()
		sclcMon, sclcPlu = self.stronglyConnectedLoopedComponents()
		nodeToComp = {}
		sclcMonNodes = []
		sclcPluNodes = []
		sclcNodes = []
		for c in sclcPlu:
			for n in c:
				sclcNodes+= [n]
				sclcPluNodes+= [n]
				nodeToComp[n] = c
		for c in sclcMon:
			for n in c:
				sclcNodes+= [n]
				sclcMonNodes+= [n]
				nodeToComp[n] = n
		ncNodes = []
		for n in nl:
			if n not in sclcNodes:
				ncNodes += [n]
				nodeToComp[n] = n
		#now we have a list of all nodes that do not belong to a sclc, 
		#of all nodes that do belong to a sclc
		#and one for each of the two types of sclcs
		# next step: generate a gSOA
		newEdges = {}
		for e in self.succ:
			for t in self.succ[e]:
				#if nodeToComp[e]!=nodeToComp[t]:
				if nodeToComp[e] not in newEdges:
					newEdges[nodeToComp[e]] = [nodeToComp[t]]
				elif nodeToComp[t] not in newEdges[nodeToComp[e]]:
					newEdges[nodeToComp[e]] += [nodeToComp[t]]
		gsoa = SingleOccurrenceAutomaton()
		gsoa.setEdges(newEdges)
		return gsoa
		
	
	def stronglyConnectedLoopedComponents(self):
		"""
		returns a tuple consisiting of a list of single-element sclcs, and a list of multiple element scls
		"""
		scc = self.strongly_connected_components()
		sclcMon = []
		sclcPlu = []
		for c in scc:
			if len(c) > 1:
				sclcPlu += [c]
			elif (c[0] not in [self.src,self.snk]) and (c[0] in self.succ[c[0]]):
				sclcMon += [c[0]]
		return sclcMon, sclcPlu
	
	def strongly_connected_components(self):
	    """
	    Tarjan's Algorithm (named for its discoverer, Robert Tarjan) is a graph theory algorithm
	    for finding the strongly connected components of a graph.
	    Based on: http://en.wikipedia.org/wiki/Tarjan%27s_strongly_connected_components_algorithm
		taken from http://www.logarithmic.net/pfh-files/blog/01208083168/tarjan.py
	    """

	    index_counter = [0]
	    stack = []
	    lowlinks = {}
	    index = {}
	    result = []

	    def strongconnect(node):
	        # set the depth index for this node to the smallest unused index
	        index[node] = index_counter[0]
	        lowlinks[node] = index_counter[0]
	        index_counter[0] += 1
	        stack.append(node)

	        # Consider successors of `node`
	        try:
	            successors = self.succ[node]
	        except:
	            successors = []
	        for successor in successors:
	            if successor not in lowlinks:
	                # Successor has not yet been visited; recurse on it
	                strongconnect(successor)
	                lowlinks[node] = min(lowlinks[node],lowlinks[successor])
	            elif successor in stack:
	                # the successor is in the stack and hence in the current strongly connected component (SCC)
	                lowlinks[node] = min(lowlinks[node],index[successor])

	        # If `node` is a root node, pop the stack and generate an SCC
	        if lowlinks[node] == index[node]:
	            connected_component = []

	            while True:
	                successor = stack.pop()
	                connected_component.append(successor)
	                if successor == node: break
	            component = tuple(connected_component)
	            # storing the result
	            result.append(component)

	    for node in self.succ:
	        if node not in lowlinks:
	            strongconnect(node)

	    return result

	def identifier(self,node):
		if node==self.src:
			return "src"
		elif node==self.snk:
			return "snk"
		elif isinstance(node,str):
			return node
		else:
			s = str(node[0])
			for i in range(1,len(node)):
				s+='X'+node[i]
			return s

	def labelify(self,node):
		if node==self.src:
			return ''
		elif node==self.snk:
			return ''
		elif isinstance(node,str):
			return node
		else:
			s = '('+str(node[0])
			for i in range(1,len(node)):
				s+=','+node[i]
			s+=')'
			return s

	def dotNodeString(self,node):
		if node in [self.src,self.snk]:
			return self.identifier(node)+'[shape=\"point\"];\n'
		else:
			return self.identifier(node)+'[shape=\"rectangle\",label=\"'+self.labelify(node)+'\"];\n'
	
	def chare(self):
		gen = generalizedSingleOccurrenceAutomaton()
		gen.setEdges(self.contractSCLC().succ)
		return gen.chare()
		
	def contract(self,contractees,label):
		if dbmode:
			print('Contracting',contractees,'in',self.succ,'to',label)
		newsucc = {}
		for e in self.succ:
			if e in contractees:
				eLab = label
			else:
				eLab = e
			for t in self.succ[e]:
				if (e not in contractees) or (t not in contractees):
					if t in contractees:
						tLab=label
					else:
						tLab=t
					if eLab not in newsucc:
						newsucc[eLab]=[tLab]
					else:
						if tLab not in newsucc[eLab]:
							newsucc[eLab]+=[tLab]
		self.succ=newsucc
		return label

	def extract(self,extractees):
		if dbmode:
			print('Extracting',extractees,'from',self.succ)
		if extractees==[]:
			newsucc = {self.src:self.snk}
		else:
			newsucc = {}
			for o in self.succ: # iterate over all possible origins:
				if o in extractees:
					olab = o
				else:
					olab = self.src
				for t in self.succ[o]:
					#print('t:',t)
					if t in extractees:
						tlab = t
					else:
						tlab = self.snk
					if (o in extractees) or (t in extractees):
						#print('new edge',o,t)
						if olab not in newsucc:
							newsucc[olab] = [tlab]
						elif tlab not in newsucc[olab]:
							newsucc[olab]+=[tlab]
		result = SingleOccurrenceAutomaton()
		result.setEdges(newsucc)
		if dbmode:
			print('Extract created',result.succ)
		return result
		
	def first(self):
		"""returns all vertices v such that the only predecessor of v is the source"""
		cand = {}
		for t in self.succ[self.src]:
			cand[t]=True
		for e in self.succ:
			if e!=self.src:
				for t in self.succ[e]:
					if t in cand:
						cand[t]=False
		f = []
		for c in cand:
			if cand[c]:
				f+=[c]
		if dbmode:
			print("First set is",f)
		return f
	
	def addEpsilon(self):
		firsts = self.first()
		newT = []
		epsNode = 'epsilon'+str(self.epscount)
		self.epscount = self.epscount + 1
		for t in self.succ[self.src]:
			if t in firsts:
				newT += [t]
			else:
				if epsNode not in newT:
					newT+= [epsNode]
				if epsNode not in self.succ:
					self.succ[epsNode]=[t]
				else:
					self.succ[epsNode]+=[t]
		self.succ[self.src]=newT
	
	def reach(self,start):
		"""returns set of all nodes that are reachable from <start>"""
		checkNodes=[start]
		marked=[start]
		reachable=set([])
		while checkNodes!=[]:
			newNodes=[]
			for n in checkNodes:
				for t in self.succ[n]:
					reachable.add(t)
					if t not in marked:
						marked += [t]
						if t!=self.snk:
							newNodes+=[t]
			checkNodes=newNodes
		return reachable
	
	def reachableAvoiding(self,start,end,avoid):
		"""returns true iff <end> can be reached from <start> without passing nodes from <avoid>"""
		checkNodes = [start]
		visited = [start]
		success = False
		while checkNodes!=[] and not success:
			newNodes = []
			for i in checkNodes:
				for t in self.succ[i]:
					if t==end:      # arrived at snk, done
						success = True
					elif (t not in avoid) and (t!=self.snk) and (t not in visited): #if t is a good node and was not checked: add to list
						newNodes += [t]
						visited += [t]
				checkNodes = newNodes
		# if dbmode:
		# 	print('And the result for',end,' is:',success)
		return success
	
	def exclusive(self,node):
		if dbmode:
			print('Computing exclusive for',node)
		cand = []
		for c in self.succ:
			if (c!=node) and self.reachableAvoiding(node,c,[]):
				cand+=[c]
		res = []
		for c in cand:
			if not self.reachableAvoiding(self.src,c,[node]):
				res += [c]
		if dbmode:
			print('Exclusives are',res)
		return res
			
	def bend(self):
		if dbmode:
			print("Calling bend on"+str(self.succ))
		#compute W
		visited = [self.src,self.snk]
		toBeChecked = []
		W = []
		for n in self.succ:
			if self.snk in self.succ[n]:
				visited = visited + [n]
				toBeChecked = toBeChecked+[n]
				W = W+[n]

		while len(toBeChecked) > 0:
			n = toBeChecked.pop()
			ssr = False # ssr: Successor of Source Reachable
			for t in self.succ[n]:
				if t in self.succ[self.src]:
					ssr=True
				elif t not in visited:
					visited += [t]
					toBeChecked += [t]						
			if ssr==True:
				W = W + [n]
		if dbmode:
			print("Computed W as "+str(W))

		# bend transitions from elements of W to succ of src
		newSucc = {}
		for n in self.succ:
			if n not in W: 
				newSucc[n] = self.succ[n]
			else:
				for t in self.succ[n]:
					if t in self.succ[self.src]:
						targ = self.snk
					else:
						targ = t
					if n in newSucc:
						if targ not in newSucc[n]:
							newSucc[n]+=[targ]
					else:
						newSucc[n]=[targ]
		self.setEdges(newSucc)
		if dbmode:
			print('Bending created',self.succ)
		
	def sore(self):
		if dbmode:
			print('Creating sore for',self.succ)
		if len(self.succ)==1:
			if dbmode:
				print('Case 1',self.succ)
			return ''
		else:
			sclcMon,sclcPlu = self.stronglyConnectedLoopedComponents()
			if len(sclcPlu)>0:
				U = sclcPlu[0]
			elif len(sclcMon)>0:
				if dbmode:
					print("small SCLCs found:",sclcMon)
				U = [sclcMon[0]]
			else:
				U=[]

			if len(U)>0: # line 4 in paper
				if dbmode:
					print('Case 2')
					print('U is',U)
				B = self.extract(U)
				B.bend()
				#print 'Bend resulted in'+str(B.succ)+' -- this will be sorified next'
				bs = B.sore()
				self.contract(U,'('+bs+')+')
				#s = self.sore()
				#print('Case 2 created',s)
				#return s
			else:
				firstSet = self.first()
				if set(self.succ[self.src])!=set(firstSet): # line 8 in paper
					if dbmode:
						print('Case 3')
					self.addEpsilon()
					#return '' # should we return here?
				elif len(firstSet)==1:#line 10 in paper
					if dbmode:
						print('Case 4')
					v = firstSet[0]
					U = [self.snk]
					for n in self.succ:
						if n!=self.src and n!=v:
							U+=[n]
					x = self.extract(U)
					if dbmode:
						print('recursing on soa', x.succ)
					l = self.labelify(v)
					lprime = x.sore()
					if lprime != '':
						l = l +',('+lprime+')'
					return l
				else: 
					# try to find v in firstSet with self.exclusive(v)!=[v]
					v = None
					for c in firstSet:
						if self.exclusive(c) not in [[c],[]]:
							v=c
							break
					if v != None: #line 16 in paper
						if dbmode:
							print('Case 5')
						U = self.exclusive(v)
						if v not in U:
							U+=[v]
						self.contract(U,'('+self.extract(U).sore()+')')
						#return self.sore()
					else: #line 20 in paper
						if dbmode:
							print('Case 6')
						maxIntersection = 0
						maxU = None
						maxV = None
						for u in firstSet:
							uset = self.reach(u)
							for v in firstSet:
								if v != u:
									vset = self.reach(v)
									cap = uset & vset
									if len(cap)>maxIntersection:
										maxIntersection = len(cap)
										maxU = u
										maxV = v
						if maxIntersection > 0:
							labU = self.labelify(maxU)
							labV = self.labelify(maxV)
							if labU == 'epsilon0':
								lab = '('+labV+')?'
							elif labV== 'epsilon0':
								lab = '('+labU+')?'
							else:
								lab = '('+labU+'|'+labV+')' 
							self.contract([maxU,maxV],lab)
							#return(self.sore())
						else:
							print("AAAAAARGH ERROR ERROR ERROR")
							return 'FUUUUUUUUUUUUU'
		return self.sore()

class generalizedSingleOccurrenceAutomaton(SingleOccurrenceAutomaton):
	"""A class for generalized single occurrence automata (SOA)"""
	src = 0
	snk = 1
	# src = 'DDFysInappropriateSrcConstant'
	# snk = 'DDFysInappropriateSnkConstant'

	def __init__(self):
		self.succ = {}
		self.pred = {}
		self.plussed = {}
		self.trivial = {}
		self.level = {}
		self.lnum = 0 # Zahl der interessanten Level (also ohne src und snk)
		self.skip = {}

	def setEdges(self,edgeblob):
		self.plussed[self.src]=False
		self.plussed[self.snk]=False
		for e in edgeblob:
			if isinstance(e,str):
				self.trivial[e]=True
			else:
				self.trivial[e]=False
			self.plussed[e]=False
			for t in edgeblob[e]:
				if t==e:
					self.plussed[e]=True
					self.trivial[e]=False
				else:
					if e not in self.succ:
						self.succ[e]=[t]
					else:
						self.succ[e]+=[t]


	def labelify(self,node):
		if node==self.src:
			return "src"
		elif node==self.snk:
			return "snk"
		
		if isinstance(node,str):
			nodestr = node
		else:
			s = '('+str(node[0])
			for i in range(1,len(node)):
				s+='|'+node[i]
			s+=')'
			nodestr=s
		if self.plussed.get(node,False):
			nodestr+='+'
		return nodestr
		
	def getTopolSort(self):
		# geklaut von http://alda.iwr.uni-heidelberg.de/index.php/Graphen_und_Graphenalgorithmen#Zwei_Algorithmen_zum_Finden_der_topologischen_Sortierung
		# eigentlich sollte das gleich beim Tarjan erledigt werden, bin aber zu faul
		result = []                          
		visited = {}
		def visit(node):                         
			if not visited.get(node,False):                
				visited[node] = True             
				if node in self.succ:
					for child in self.succ[node]:     
						visit(child)
				result.append(node)              
		visit(self.src)
		result.reverse()
		return result

	def computePred(self):
		for orig in self.succ:
			for target in self.succ[orig]:
				if target in self.pred:
					self.pred[target]+=[orig]
				else:
					self.pred[target]=[orig]


	def constructLevelOrder(self):
		self.computePred()
		lvl = {}
		lvl[self.src]=0
		tops = self.getTopolSort()
		for n in tops[1:]:
			lvl[n]=max([lvl[s] for s in self.pred[n]])+1
		for node in lvl:
			if lvl[node] not in self.level:
				self.level[lvl[node]]=[node]
			else:
				self.level[lvl[node]]+=[node]	
		self.lnum = len(self.level)-1
		#determine skiplevels: should be more efficient (check every edge only once)
		for l in range(1,self.lnum):
			self.skip[l]=False
		for e in self.succ:
			for t in self.succ[e]:
				if lvl[t]>lvl[e]+1:
					for l in range(lvl[e]+1,lvl[t]):
						self.skip[l]=True

	def getTrivials(self,l):
		res=list(filter(lambda x: self.trivial.get(x,False),self.level[l]))
		return res
	
	def chare(self):
		self.constructLevelOrder()
		res = ''
		for l in range(1,self.lnum):
			C = self.getTrivials(l) # trivial nodes
			B = list(filter(lambda x: x not in C,self.level[l])) # non trivial nodes
			for a in B:
				res += self.labelify(a)
				if self.skip[l] or (len(B)+len(C)>1):
					res += '?'
			if len(C)>0:
				if len(C)==1:
					res += C[0]
				else:
					res += '('+str(C[0])
					for i in range(1,len(C)):
						res+='|'+C[i]
					res+=')'
				if self.skip[l] or (len(B)>0):
					res += '?'
			if l < self.lnum-1:
				res += ', ' # comma between levels to highlight poss of switching		
		return res.replace('+?','*')
		

# soa.addString("acab")
# soa.addString("ac")
# soa.addString("c")
# soa.addString("abgf")
# soa.addString("adgbeeff")

# soa.addString(["haus","auto","haus","boot"])
# soa.addString(["haus","boot","boot"])

# soa.addString("ccdf")
# soa.addString("af")
# soa.addString("ababef")

# soa = SingleOccurrenceAutomaton()
# soa.addString("bca")
# soa.addString("bada")
# 
# elt='BOB'
# 
