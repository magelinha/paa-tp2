# -*- coding: utf-8 -*-
"""
Created on Thu Nov 13 23:20:18 2014

@author: LuizF
"""
import sys
sys.path.append('..\\')

import reader

class Q1:
    """ Class implementing naive backtracking """
    gDebug = True
    def __init__(self):
        self.dimension = None
        self.minCostPath = []
        self.minCostValue = float("inf")
        self.enumTreeSize = 0
        self._distanceMatrix = []
        self._fileLoader = reader.FileReader()


    # Solution based on Programming Challenges Textbook
    # Generating all permutations and computing TSP
    def Backtracking(self, a, k, n):
        c = [None]*self.dimension
        ncandidates = None
        if k == n:
            cost = self._ProcessSolution(a,k,n)
            self.enumTreeSize += 1
            if cost < self.minCostValue:
                self.minCostValue = cost
                self.minCostPath = a.copy()
        else:
            k = k + 1
            c, ncandidates = self._ConstructCandidates(a,k,n,c)
            for i in range(ncandidates):
                a[k] = c[i]
                self.Backtracking(a,k,n)

    # Sanity check - example: http://goo.gl/bnYyaV
    def LoadSimpleTest(self):
        self._Clear()
        self.dimension = 5
        dist = [None]*self.dimension
        dist[0] = [None,3,1,5,8]
        dist[1] = [3,None,6,7,9]
        dist[2] = [1,6,None,4,2]
        dist[3] = [5,7,4,None,3]
        dist[4] = [8,9,2,3,None]
        self._distanceMatrix = dist.copy()
        if self.gDebug:
            for v in dist:
                print(v)

    def LoadFile(self,id):
        self._Clear()
        self._fileLoader.OpenFile(id)
        self.dimension = self._fileLoader.GetElemNumber()
        self._distanceMatrix = self._fileLoader.GetDistanceMatrix().copy()

    # A posição do vetor a[0] nunca é utilizada, portanto teremos o valor False
    # Já possuímos um elemento na solução, que é o elemento inicial a[1] = 1
    # Portanto, k = 1
    # Com isto temos (n-1)! permutações a serem calculadas (ao invés de n!)
    def DoBacktracking(self):
        self.minCostPath = []
        self.minCostValue = float("inf")
        self.enumTreeSize = 0
        n = self.dimension
        a = [False]*(n+1)
        k = 1
        a[1] = 1
        self.Backtracking(a,k,n)
        self.minCostPath.append(1)

    def _Clear(self):
        self.dimension = None
        self._distanceMatrix.clear()


    def _ProcessSolution(self, a,k,n):
        cost = 0

        if self.gDebug:
            print('Path:', end='')
            for i in range(1,k+1):
                    print('', a[i], end='')

        if self.gDebug:
            print(' Weight:', end='')

        for i in range (1, k):
            if self.gDebug:
                print('', self._Distance(a[i], a[i + 1]), end='')
            cost += self._Distance(a[i], a[i + 1])

        cost += self._Distance(a[k],a[1])
        if self.gDebug:
            print('', self._Distance(a[i], a[i + 1]), end='')
            print(' Cost: ', cost )
            print('')

        return cost

    def _ConstructCandidates(self,a,k,n,c):
        in_perm = [False]*(self.dimension + 1)
        for i in range(k):
            in_perm[a[i]] = True

        ncandidates = 0
        for i in range(1, n + 1):
            if in_perm[i] == False:
                c[ncandidates] = i
                ncandidates = ncandidates + 1
        return c,ncandidates

    def _Distance(self,x,y):
        i,j = (x - 1),(y - 1)
        if i > self.dimension or j > self.dimension or i < 0 or j < 0:
            print("Erro")
            return None
        return self._distanceMatrix[i][j]




bt = Q1()
#bt.LoadFile(0)
bt.LoadSimpleTest()
bt.DoBacktracking()

def test(t):
    bt.DoBacktracking()


#import timeit
#print(timeit.timeit("test()", setup="from __main__ import test", number=1))

print('Best Tour: Cost', bt.minCostValue)
print('Path', bt.minCostPath)
print('Enum Tree size', bt.enumTreeSize)