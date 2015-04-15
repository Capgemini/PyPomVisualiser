'''
Created on 14 Apr 2015

@author: WMOORHOU
'''
from abc import ABCMeta, abstractmethod

class Display:
    __metaclass__ = ABCMeta
    
    @abstractmethod
    def drawSquare(self, x_loc, y_loc, width, height, colour=None, content=None):
        pass
    
    @abstractmethod
    def drawCircle(self, x_loc, y_loc, width, height, colour=None, content=None):
        pass
    
    @abstractmethod
    def drawLine(self):
        pass
    
    @abstractmethod
    def runDisplay(self):
        pass
        
    @abstractmethod    
    def remove(self, num):
        pass