#!/usr/bin/env python
# -*- coding: utf-8 -*-

#Created by João Victor Magela
from MGraph import Graph
from MFibonacciHeap import *
import sys, time


def dijsktra(graph, initial):
	"""
	A variável map_key é uma variante para a busca em um heap de fibonacci.
	A busca e alteração de itens nesse mapa é O(1)

	A inicialização insere todos os elementos com distância inicial 'infinito', 
	com exceção do nó inicial, cujo valor é 0
	"""
	fb = FibonacciHeap();
	map_key = {initial: 0}
	
	for node in graph.nodes:
		if node != initial:
			map_key[node] = fb.insert(node, sys.maxsize)
		else:
			map_key[node] = fb.insert(node, 0)
			
	path = {}

	nodes = set(graph.nodes)

	while nodes:
		"""
		Para pegar o menor elemento, basta extrair o mínimo do heap.
		"""
		min_node = fb.extract_minimum()
		
		if min_node is None:
			break
 
		nodes.remove(min_node.key)
		current_weight = min_node.value
 
		"""
		A operação de atualização é feita através do decrease_key. 
		""" 
		for edge in graph.edges[min_node.key]:
			weight = current_weight + graph.distances[(min_node.key, edge)]
			if weight < map_key[edge].value:
				fb.decrease_key(map_key[edge], weight)
				map_key[edge].value = weight
				path[edge] = min_node.key

	return map_key,fb, path		

def print_mapKey(map_key):
	print ("\n\nmap_key")
	for item in map_key:
		print ((item, map_key[item].value))
	print ("map_key\n")
	
#Leitura de arquivo. Segue os seguintes passos:
#1 - Faz a leitura de todas as linhas do arquivo
#2 - Procura pela linha que simboliza o número de nós
#3 - Cria os nós do grafo
#4 - Percorre as linhas do arquivo criar as arestas entre os vértices
def preencherGrafo(grafo, arquivo):
	dados = arquivo.readlines()
	end = False
	for linha in dados:
		divisao = linha.split( ) 
		
		if not divisao:
			continue
			
		if divisao[0] == "Nodes":
			qtdNodes = int(divisao[1])
			print ("Quantidade de nós a serem criados: %d\n" % qtdNodes)
			
			criarNos(grafo,qtdNodes)
			end = True
		elif divisao[0] == "E":
			#se encontrar um "E", indica que é a uma aresta
			grafo.add_edge(int(divisao[1]), int(divisao[2]), int(divisao[3]))
		elif end == True and divisao[0] == "End":
			#se achar um End depois de linhas que simbolizam aresta, encerra a função.
			arquivo.close()
			return

#adiciona os vertices em um grafo. Os vertices vão de 0 até qtdNodes-1		
def criarNos(grafo, qtdNodes):
	for i in range(qtdNodes):
		grafo.add_node(i+1)

if __name__ == "__main__":
	grafo = Graph()
	arquivo = open("../../DMXA/2500x3125/e01.stp", 'r')
	
	preencherGrafo(grafo,arquivo)
	
	cont = init = end = 0
	sumTime = 0.
	
	while (sumTime < 5.0):		
		init = time.process_time()
		sizes,fb, path = dijsktra(grafo,1)
		end = time.process_time()
		
		sumTime = sumTime + end - init
		cont = cont + 1
	print ("executou na média de: %f" % (sumTime/cont))
	
	arquivo = open("../../DMXA/resultados_2500x3125.txt", 'a')
	arquivo.write("FibonacciHeap\t" + str(sumTime/cont) + "\t" + str(cont) + "\n")
	arquivo.close()
	
	"""
	for item in sizes:
		print sizes[item].value
	"""
