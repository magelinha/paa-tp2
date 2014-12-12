#!/usr/bin/env python
# -*- coding: utf-8 -*-

#Created by João Victor Magela

"""
	Implementação do q-rota
"""

import sys,copy
from heapq import heappush, heappop
from MGraph import Graph
import file_reader

minTour = sys.maxsize

class Node:
	#deve ser informado o último vértice do conjunto já visitado
	def __init__(self, last):
		self.level = 0 #nível da árvore de enumeração
		self.length = 0 #tamanho do caminho
		self.bound = 0.0 #bound do nó
		self.lastVertex = last #ultimo nó da 
		self.path = []
		self.S = []

	def __lt__(self, other):
		return self.bound < other.bound

class TspBB:
	def __init__(self, graph):
		self.graph = graph #grafo a ser usado
		self.infity = sys.maxsize #simulação de um valor infinito
		self.sizeGraph = len(graph.nodes) #quantidade de itens do grafo
		self.heap = [] #simula um heap binário
		self.minTour = sys.maxsize
		self.bestTour = []

	def tsp(self):
		while self.heap:
			temp = heappop(self.heap)

			if(temp.bound < self.minTour):
				#gera um novo nível com todos os vizinhos do item, desconsiderando os que já foram visitados
				for nextVertex in self.graph.edges[temp.lastVertex]: 
					if nextVertex not in temp.path: #desconsidera se o vértice já faz parte da permutação parcial
						
						#cria um novo nó para o heap, adicionado o nível, tamanho e caminho atual
						newNode = Node(nextVertex)
						newNode.level = temp.level + 1
						newNode.length = temp.length + self.graph.distances[(temp.lastVertex, nextVertex)]
						
						#lista com a caminho atual já percorrido
						newNode.path = copy.deepcopy(temp.path)
						newNode.path.append(nextVertex)

						#conjunto de itens que ainda não foram visitados
						newNode.S = copy.deepcopy(temp.S)
						newNode.S.remove(nextVertex)

						#executado quando falta apenas um 1 item para adicionar no path
						if(newNode.level == self.sizeGraph - 2):
							for node in self.graph.edges[nextVertex]:
								if node not in newNode.path:
									newNode.path.append(node)
									newNode.length = newNode.length + self.graph.distances[(nextVertex, node)]

									#completa o tour, voltando para o nó inicial
									newNode.path.append(newNode.path[0])
									newNode.length = newNode.length + self.graph.distances[(node, newNode.path[0])]

									if newNode.length < self.minTour:
										self.minTour = newNode.length
										self.bestTour = copy.deepcopy(newNode.path)

									break
						#o else indica que é um tour parcial, então deve ser calculado o lower bound
						else:
							newNode.bound = self.lowerBoundQRota(nextVertex, len(temp.S) - 1, temp.lastVertex, temp.S)
							if newNode.bound < self.minTour:
								heappush(self.heap, newNode)


	"""
		w = vértice final
		k = tamanho do conjunto
		S = conjunto
		v = ultimo elemento da permutação parcial
	"""
	def lowerBoundQRota(self, w, k, v, S):
		resultados = []
		menor = sys.maxsize

		if k == 0:
			return self.graph.distances[(v,w)]
		for node in S:
			menor = min(menor, graph.distances[(node, w)]  + self.lowerBoundQRota(node, k-1, v, S))
		return menor + graph.distances[(w, 0)]


def createGraph(id):
        graph = Graph()

        """
        reader = file_reader.FileReader()
        reader.OpenFile(id)
        dimension = reader.GetElemNumber()
        distancesMatrix = reader.GetdistancesMatrix().copy()
        """
        dimension = 5
        dist = [None]*dimension
        dist[0] = [None,3,1,5,8]
        dist[1] = [3,None,6,7,9]
        dist[2] = [1,6,None,4,2]
        dist[3] = [5,7,4,None,3]
        dist[4] = [8,9,2,3,None]
        distanceMatrix = dist.copy()
        
        for i in range(dimension):
        	graph.add_node(i)

        for i in range(len(distanceMatrix)):
        	for j in range(len(distanceMatrix[i])):
        		if i==j:
        			graph.add_edge(i,j,0)
        		else:
        			graph.add_edge(i,j,distanceMatrix[i][j])

        return graph

if __name__ == "__main__":

	"""
	Aqui deve ser criado o grafo a ser passado para o tsp
	"""

	graph = createGraph(0)
	tspBB = TspBB(graph)
	root = Node(0) #o vértice inicial sempre será o 0
	root.path.append(0)
	root.S = copy.deepcopy(graph.nodes)
	root.S.remove(0)
	root.bound = tspBB.lowerBoundQRota(0, len(root.S)-1, 0, root.S)

	heappush(tspBB.heap, root)
	tspBB.tsp()

	print (tspBB.minTour) #resultado final