import sys
import weakref

# A node in the Fibonacci heap.
class Node:
	def __init__(self, key, value, parent=None):
		
		self.key = key
		self.value = value
		
		self.parent = weakref.ref(parent) if parent else parent
		self.children = []
		self.marked = False
		
# A Fibonacci heap.
class FibonacciHeap:
	def __init__(self):
		
		self.roots = set()
		self.minimum = None
		
	def is_empty(self):
		return len(self.roots) == 0
	
	def clear(self):
		self.roots = set()
		self.minimum = None
		
	def find_minimum(self):
		"""This is an internal function that the user should never have to call.
		From the user's perspective it should be a somewhat expensive no-op."""
		
		if len(self.roots) == 0:
			self.minimum = None
			return
		for n in self.roots:
			if self.minimum == None or n.value < self.minimum.value:
				self.minimum = n
	
	# Merges this heap with another heap.
	def merge(self, other):
		"""Merges this heap with FibonacciHeap "other".  After the merge,
		the nodes from both heaps will be contained in this heap."""
		
		# Add the other heap's roots
		self.roots &= other.roots
		# The minimal node is one of our minimum or the other's minimum.
		if len(self.roots) == 0:
			self.minimum = None
			return
		if self.minimum == None:
			self.minimum = other.minimum
			return
		if other.minimum == None:
			return
		if other.minimum.value < self.minimum.value:
			self.minimum = other.minimum
		
	# Inserts a new node into the heap with the given key and data.  Returns
	# the new FibonacciNode created.
	def insert(self, key, value):
		
		# Just make a node and add it to the roots.
		n = Node(key,value)
		self.roots.add(n)
		
		# Update minimum if appropriate
		if self.minimum == None or n.value < self.minimum.value:
			self.minimum = n
		return n
		
	# Returns the minimal node (key, data) but does not remove it.
	def peek_minimum(self):
		"""Returns the (key, data) pair of the minimally-valued FibonacciNode
		in the heap, but does not remove the min-node."""
		
		return self.minimum
		
	# Removes and returns the minimal node (key, data) in the heap.
	def extract_minimum(self):
		"""Returns the (key, data) pair of the minimally-valued FibonacciNode
		in the heap, and removes that node from the heap.  Operates in
		amortized O(log n) time."""
		
		# Grab the minimal node
		if self.minimum == None: return None
		m = self.minimum
		
		# Remove the minimal node, reset the reference to it, and
		# reparent its children to be root nodes.
		try:
			self.roots.remove(m)
		except:
			
			print ('minimum is',m.key,',',m.value)
			for r in self.roots:
				print ('root',r.key,',',r.value)
			raise
		self.minimum = None
		for c in m.children:
			c.parent = None
			c.marked = False
			self.roots.add(c)
		m.children = []
		
		# Iterate over the root list, checking for nodes with the same degree.
		# When nodes with the same degree are found, make the one with the
		# larger key a child of the other.
		# Repeat until no roots with the same degree exist.
		collision = True
		while collision:
			# Map from degree values to root nodes
			degreeDict = {}
			# not safe to remove from an iterable while we iterate over it.
			# Thus keep a set of nodes to be removed and take them all out
			# at the end.
			removedRoots = set()
			for n in self.roots:
				deg = len(n.children)
				if deg in degreeDict:
					if degreeDict[deg].value < n.value:
						smaller = degreeDict[deg]
						larger = n
					else:
						smaller = n
						larger = degreeDict[deg]
					smaller.children.append(larger)
					larger.parent = weakref.ref(smaller)
					degreeDict[deg] = smaller
					removedRoots.add(larger)
				else:
					degreeDict[deg] = n
			collision = (len(removedRoots) != 0)
			self.roots -= removedRoots
		
		# Find the new minimum node
		self.find_minimum()
		# Return the old minimum node
		return m
		
	# An internal operation -- should never be called by the user!
	#
	# Removes given node from its parent, makes it a root node, and returns
	# the parent node.
	def cut_node(self, node):
		"""This is an internal function.  Users should NEVER call this function,
		as it will probably violate all kinds of heap properties."""
		
		if node.parent == None:
			raise RuntimeError("Node to be cut is already root")
		p = node.parent()
		p.children.remove(node)
		node.parent = None
		node.marked = False
		self.roots.add(node)
		if node.value < self.minimum.value:
			self.minimum = node
		return p
		
	def decrease_key(self, node, value):
		"""Decreases the key on the given node to the new value.  Operates in
		amortized constant time."""
		
		if value >= node.value:
			return
		
		node.value = value
		if node.parent == None:
			if node.value < self.minimum.value:
				self.minimum = node
			return
		if node.value >= node.parent().value:
			return
		
		n = self.cut_node(node)
		while n.marked:
			n = self.cut_node(n)
		
		if n.parent != None:
			n.marked = True
			
	def delete(self, node):
		"""Deletes the given node from the tree.  Operates in amortized O(log n)
		time."""
		self.decrease_key(node, sys.float_info.min)
		self.extract_minimum()
