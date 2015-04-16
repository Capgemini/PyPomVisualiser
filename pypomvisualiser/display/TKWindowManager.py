'''
Created on 9 Apr 2015

@author: WMOORHOU
'''

from pypomvisualiser.display.DisplayFactory import DisplayFactory
from pypomvisualiser.pom.PomParser import NodeEnum
import calendar
import time
import random

class WindowManager(object):
    '''
    classdocs
    '''
    
    def __init__(self):
        self.rendered=dict()
        self.toBeRendered=[]
        self.spacing = 11
        self.baseSize = 10
        self.scale = 10
        self.focus = None
        self.levelCounter = dict()
        self._display = DisplayFactory.getDisplayMechanism()
        self.spacing = self.scale * (self.spacing * 1.5) 
        self.baseSize = self.scale * self.baseSize
        '''
        Constructor
        '''
    
    def drawNode(self, level, node):
        if not self.isNodeRendered(node):
            if level not in self.levelCounter:
                self.levelCounter[level] = 0
            else:
                self.levelCounter[level] = self.levelCounter[level] + 1
            x_loc = self.levelCounter[level]*self.spacing
            y_loc = (level+1)*self.spacing
            width = self.baseSize * 1.5
            
            # Need to make a tag tuple
            tags = self.getTagTuple(node, level)
            
            if node.getType() == NodeEnum.ROOTPOM:
                self.rendered[node] = tags
                self._display.drawSquare(x_loc, y_loc, width, self.baseSize, tags, node.getType().value, node.toString())
            else:
                self.rendered[node] = tags
                self._display.drawCircle(x_loc, y_loc, width, self.baseSize, tags, node.getType().value, node.toString())
            self._display.drawTextInId(self.rendered[node][0], tags, node.toShortString(), node.toString())
    
    def connectNodes(self, master, slave):
        masterId = self.rendered.get(master)
        slaveId = self.rendered.get(slave)
        if masterId and slaveId:
            nodeTypeValue = slave.getType().value
            # Queue for creation, then organise once all nodes created.
            def toRender(masterId=masterId, slaveId=slaveId, nodeTypeValue=nodeTypeValue):
                return self._display.connectIdWithLine(masterId[0], slaveId[0], masterId[1] + masterId[2] + slaveId[1] + slaveId[2], nodeTypeValue)
            self.addToRenderLaterList(toRender)
        else:
            print("Node values could not be extracted from render list, no joining will be done")        
    
    def generateUniqueTag(self, node):
        return str(node.getType()) + str(calendar.timegm(time.gmtime())) + str(random.random())
    
    def getTagTuple(self, node, level):
        unique = self.generateUniqueTag(node)
        nodeType = str(node.getType())
        level = "level"+str(level)
        return (unique, nodeType, level)
    
    def populateMenu(self):
        #Hide node
        pass
    
    def addToRenderLaterList(self, function):
        self.toBeRendered.append(function)
    
    def renderFromLaterList(self):
        for func in self.toBeRendered:
            func()
    
    def isNodeRendered(self, node):
        if node in self.rendered:
            return True
        else:
            return False
    
    def organiseNodeRendering(self):
        
        highVal = 0
        for key, value in self.levelCounter.items():
            print (key)
            if value > highVal:
                highVal = value
        
        # work out offset
        highValOffset = (highVal/2) * self.spacing
        
        for key, value in self.levelCounter.items():
            if value != highVal:
                levelOffsetValue = highValOffset - ((value/2) * self.spacing)
                self._display.move("level"+str(key), levelOffsetValue, 0)
        
        #self focus on root node
        pass    
    
    def finalise(self):
        self.organiseNodeRendering()
        self.renderFromLaterList()
        self._display.runDisplay()
        pass