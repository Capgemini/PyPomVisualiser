'''
Created on 31 Mar 2015

@author: WMOORHOU
'''
from os import name

from src.display.TKinterDisplay import *

class DisplayFactory(object):
    '''
    classdocs
    '''
    @staticmethod
    def getDisplayMechanism():
        if name is "nt":
            display = TKinterDisplay()
            return display
        else:
            '''Not nt therefore likely to be posix'''
            return
        
        
from abc import ABCMeta, abstractmethod

class Display:
    __metaclass__ = ABCMeta
    
    @abstractmethod
    def drawSquare(self, x_loc, y_loc, width, height, colour=None, function=None):
        pass
    
    @abstractmethod
    def drawCircle(self, x_loc, y_loc, width, height, colour=None, function=None):
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