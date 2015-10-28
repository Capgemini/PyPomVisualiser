'''
Created on 14 Apr 2015

@author: WMOORHOU
'''
from abc import ABCMeta, abstractmethod

class Display:
    __metaclass__ = ABCMeta
    
    @abstractmethod
    def drawSquare(self, xywhTuple, tags=None, colour=None, content=None):
        pass
    
    @abstractmethod
    def drawCircle(self, xywhTuple, tags=None , colour=None, content=None):
        pass
    
    @abstractmethod
    def connectIdWithLine(self, id1, id2, tags=None, colour=None):
        pass
    
    @abstractmethod
    def renderTextInId(self, tagTocentreOn, tagsToAddTo, content, funcContent):
        pass
    
    @abstractmethod
    def move(self, tag, xamount, yamount):
        pass
    
    @abstractmethod
    def runDisplay(self):
        pass

    