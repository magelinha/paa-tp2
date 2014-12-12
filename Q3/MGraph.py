#!/usr/bin/env python
# -*- coding: utf-8 -*-

#Created by João Victor Magela

import collections, copy

class Graph:
	def __init__(self, digraph = True):
		self.nodes = set()
		self.edges = collections.defaultdict(list)
		self.distances = {}
		self.digraph = digraph
		self.maxEdge = None
		self.sumEdges = 0
		self.sumSizeEdges = 0
 
	def add_node(self, value):
		self.nodes.add(value)
 
	def add_edge(self, from_node, to_node, distance):
		if self.digraph:
			self.edges[from_node].append(to_node)
			self.edges[to_node].append(from_node)
			self.distances[(from_node, to_node)] = distance
			self.distances[(to_node, from_node)] = distance
		else:
			self.edges[from_node].append(to_node)
			self.distances[(from_node, to_node)] = distance	
		
		if self.maxEdge is None or distance > self.maxEdge:
			self.maxEdge = distance
		
		self.sumSizeEdges = self.sumSizeEdges + distance
		self.sumEdges = self.sumEdges + 1
 #fim da classe para operações com grafos.
