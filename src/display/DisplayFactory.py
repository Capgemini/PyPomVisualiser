'''
Created on 31 Mar 2015

@author: WMOORHOU
'''
from os import name

from src.display.TKinterDisplay import TKinterDisplay

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
            display = TKinterDisplay()
            return display
