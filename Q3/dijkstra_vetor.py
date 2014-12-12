#!/usr/bin/env python
# -*- coding: utf-8 -*-

#Created by João Victor Magela
from MGraph import Graph
import sys, time

def dijsktra(graph, initial):
	
	"""
	Todos as posições do vetor, com exceção da posição 
	referente ao nó inicial, recebem o valor maxsize,
	que representa o valor infinito. A posição do nó inicial
	recebe o valor 0, pois é a distância dele para ele mesmo.
	"""
	visited = [sys.maxsize for i in range(len(graph.nodes)+1)]
	visited[initial] = 0
	
	path = {}

	nodes = set(graph.nodes)
	
	"""
	Essa iteração visa encontrar o vértice mais perto do nó escolhido no passo anterior. 
	
	O processo inicial com o nó inicial e vai selecionando os nós até que não tenha mais 
	nós ou seja impossível chegar no mesmo através do nó inicial
	"""
	while nodes:
		
		#busca o nó mais perto do último nó selecionado
		min_node = None
		for node in nodes:
			if visited[node] < sys.maxsize:
				if min_node is None:
					min_node = node
				elif visited[node] < visited[min_node]:
					min_node = node

		#caso não tenha encontrado, encerra o processo
		if min_node is None:
			break
 
		
		nodes.remove(min_node)
		current_weight = visited[min_node]
 
		"""
		Atualiza a distância do nó inicial para os vizinhos do nó selecionado, caso a nova distância 
		calculada seja menor que a já existente
		"""
		for edge in graph.edges[min_node]:
			weight = current_weight + graph.distances[(min_node, edge)]
			if weight < visited[edge]:
				visited[edge] = weight
				path[edge] = min_node

	return visited, path

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
		visited, path = dijsktra(grafo,1)
		end = time.process_time()
		
		sumTime = sumTime + end - init
		cont = cont + 1
	print ("executou na média de: %f" % (sumTime/cont))
	
	arquivo = open("../../DMXA/resultados_2500x3125.txt", 'a')
	arquivo.write("Vetor\t" + str(sumTime/cont) + "\t" + str(cont) + "\n")
	arquivo.close()
	
	"""
	first = True
	print "Caminho para os nós (Nó -> Distância total)"
	for i in range(len(visited)):
		if first:
			first = False
			continue
		
		if visited[i] == sys.maxsize:
			print "%d -> infinito" % i
		else:
			print "%d -> %d" % (i,visited[i])
	
	"""
