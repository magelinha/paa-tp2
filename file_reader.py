# -*- coding: utf-8 -*-
"""
Created on Fri Nov 14 17:29:38 2014

@author: LuizF
"""

import xml.etree.ElementTree as ET
from os import listdir
from os.path import isfile, join, splitext
from re import findall

class FileReader:
    """Class to read .xml input files"""

    # Fill file list in sorted order by input size
    def __init__(self):
        self.distMatrix = []
        self.currentId = None
        self.basePath = '..\\resources'
        self.fileList = [
            f for f in listdir(self.basePath)
                if isfile(join(self.basePath,f))
                    if splitext(f)[1] == '.xml'
        ]
        print(len(self.fileList))
        self._ProcessFileList()

    # Open file and fill adjacency matrix self.distMatrix
    # File id's goes from 0 to 10
    def OpenFile(self, id):
        self.currentId = id
        if id < len(self.fileList):
            filePath = self.basePath + '\\' + self.fileList[id][1]
            tree = ET.parse(filePath)
            root = tree.getroot()
            i = 0
            for vertex in root.find('graph'):
                self.distMatrix.append([])
                j = 0
                for d in vertex:
                    if i == j:
                        self.distMatrix[i].append(None)
                    tmpValue = int(float(d.attrib.get('cost')))
                    self.distMatrix[i].append(tmpValue)
                    j+=1
                i+=1
            self.distMatrix[i-1].append(None) # Add None to last element

    def GetDistanceMatrix(self):
        return self.distMatrix
    def GetElemNumber(self):
        return self.fileList[self.currentId][0]


    # Sort files list by input size
    def _ProcessFileList(self):
        tmp = []
        for f in self.fileList:
            tmp.append(((int(findall(r'\d+', f)[0])),f))
        tmp.sort()
        self.fileList = tmp.copy()


#i = 0
#for vertex in root.find('graph'):
#    print(i, vertex)
#    for d in vertex:
#        print(int(float(d.attrib.get('cost'))), end=' ')
#    i+=1