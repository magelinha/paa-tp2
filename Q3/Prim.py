#!/usr/bin/env python
# -*- coding: utf-8 -*-

#Created by João Victor Magela

from MGraph import Graph
from MFibonacciHeap import *
import sys

def prim(graph, initial, currentPath):
	BRANCO = 'B'
	CINZA = 'C'
	PRETO = 'P'

	color= {}
	pred = {}
	visited = []
	distance = {}

	for i in graph.nodes:
		color[i] = BRANCO
		pred[i] = None
		distance[i] = sys.maxsize

	distance[initial] = 0
	pred[initial] = initial

	fila = FibonacciHeap()
	fila.insert(initial,0)

	while fila.is_empty() == False:
		v = fila.extract_minimum()
		print (v.key, v.value)
		visited.append(v.key)

		"""
		A operação de atualização é feita através do decrease_key. 
		""" 
		for node in graph.edges[v.key]:
			if node in currentPath:
				continue

			if(node not in visited and distance[node] > graph.distances[(v.key, node)]):
				pred[node] = v.key
				
				if(color[node] == BRANCO):
					#insere normalmente na heap
					fila.insert(node, graph.distances[(v.key, node)])
					color[node] = CINZA
				elif(color[node] == CINZA):
					#diminui o valor no heap
					temp = Node(node, distance[node])
					fila.decrease_key(temp, graph.distances[(v.key, node)])
				
				distance[node] = graph.distances[(v.key, node)]
				
		color[v.key] = PRETO


	return pred, calc_sum(pred, graph)		

def calc_sum(pred, graph):
	soma = 0
	for i in pred:
		soma = soma + graph.distances[(i, pred[i])]

	return soma