# -*- coding: utf-8 -*-
"""
Created on Thu Nov 13 23:20:18 2014

@author: LuizF
"""

Debug = True

length = 4

finished = False

dist = []
for i in range(length):
    dist.append([])
    for j in range(length):
        if i == j:
            dist[i].append(None)
        else:
            dist[i].append((i+1)*(j+1))

if Debug:
    for v in dist:
        print(v)

def distance(x,y):
    i,j = (x - 1),(y - 1)
    if i > length or j > length or i < 0 or j < 0:
        print("Erro")
        return None
    return dist[i][j]

MinCost = float("inf")

# Solution based on Programming Challenges Textbook
# Generating all permutations and computing TSP
def processSolution(a,k,n):
    cost = 0

    if Debug:
        print('Path:', end='')
        for i in range(1,k+1):
                print('', a[i], end='')

    if Debug:
        print(' Weight:', end='')
    for i in range (1, k):
        if Debug:
            print('', distance(a[i],a[i+1]), end='')
        cost += distance(a[i],a[i+1])

    cost += distance(a[k],a[1])
    if Debug:
        print('', distance(a[i],a[i+1]), end='')
        print(' Cost: ', cost )
        print('')
    return cost

def constructCandidates(a,k,n,c):
    in_perm = [False]*(length+1)
    for i in range(k):
        in_perm[a[i]] = True

    ncandidates = 0
    for i in range(1,n+1):
        if in_perm[i] == False:
            c[ncandidates] = i
            ncandidates = ncandidates + 1

#    if Debug:
#        print('k =',k,'<>',ncandidates,'candidatos', c)

    return c,ncandidates

def backtrack(a, k, n, MinCost):
    c = [None]*length
    ncandidates = None
    if k == n:
        cost = processSolution(a,k,n)
        if cost < MinCost:
            MinCost = cost
    else:
        k = k + 1
        c, ncandidates = constructCandidates(a,k,n,c)
        for i in range(ncandidates):
            a[k] = c[i]
#            if Debug:
#                print('k =',k,'<> S:',a)
            cost = backtrack(a,k,n, MinCost)
            if cost < MinCost:
                MinCost = cost
    return MinCost

n = length
a = [False]*(length+1)
print(backtrack(a,0,n, MinCost))
