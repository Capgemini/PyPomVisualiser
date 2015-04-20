'''
Created on 9 Apr 2015

@author: WMOORHOU
'''

from pypomvisualiser.display.DisplayFactory import DisplayFactory
from pypomvisualiser.pom.TreeCreation import NodeEnum
import calendar
import time
import random

class WindowManager(object):
    '''
    classdocs
    '''
    
    def __init__(self):
        self.rendered = dict()
        self.toBeRendered = []
        self.layoutManagement = TKLayoutManagement()
        self._display = DisplayFactory.getDisplayMechanism()
        '''
        Constructor
        '''
    
    def drawNode(self, level, node):
        if not self.isNodeRendered(node):
            tags = self.getTagTuple(node, level)
            self.rendered[node] = tags
            nodeTuple = self.layoutManagement.addNodeToLayout(level)
            if node.getType() == NodeEnum.ROOTPOM:
                self._display.drawSquare(nodeTuple, tags, node.getType().value, node.toString())
            else:
                self._display.drawCircle(nodeTuple, tags, node.getType().value, node.toString())
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
        level = "level" + str(level)
        return (unique, nodeType, level)
    
    def populateMenu(self):
        # Hide node
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
    
    def __organiseNodes(self):
        tuplelist = self.layoutManagement.getStructureOrganisationTupleList()
        for levelTuple in tuplelist:
            self._display.move(levelTuple[0], levelTuple[1], levelTuple[2])
        # self focus on root node
        pass    
    
    def finalise(self):
        self.__organiseNodes()
        self.renderFromLaterList()
        self._display.runDisplay()
        pass
    
class TKLayoutManagement(object):
    
    def __init__(self):
        self.spacing = 11
        self.baseSize = 10
        self.scale = 10
        self.spacing = self.scale * (self.spacing * 1.5) 
        self.baseSize = self.scale * self.baseSize
        self.levelCounter = dict()
        pass
    
    '''
    Creates a tuple of arguments required for coordinate locations for node rendering.
    '''
    def addNodeToLayout(self, level):
        if level not in self.levelCounter:
            self.levelCounter[level] = 0
        else:
            self.levelCounter[level] = self.levelCounter[level] + 1
        x_loc = self.levelCounter[level] * self.spacing
        y_loc = (level + 1) * self.spacing
        width = self.baseSize * 1.5
        height = self.baseSize
        return (x_loc, y_loc, width, height)
    
    '''
    Method to create a tranformational tuple to organise nodes in a more appealing arrangement. 
    Takes the largest number of nodes on a level, then compensates at every other level to centre all nodes.
    Returns a list of tuples
    '''
    def getStructureOrganisationTupleList(self):
        highVal = 0
        for key, value in self.levelCounter.items():
            print (key)
            if value > highVal:
                highVal = value
        
        # work out offset
        highValOffset = (highVal / 2) * self.spacing
        orgList = []
        for key, value in self.levelCounter.items():
            if value != highVal:
                levelOffsetValue = highValOffset - ((value / 2) * self.spacing)
                orgList.append(("level" + str(key), levelOffsetValue, 0))
        return orgList
