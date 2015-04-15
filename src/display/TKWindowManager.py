'''
Created on 9 Apr 2015

@author: WMOORHOU
'''

from src.display.DisplayFactory import DisplayFactory

class WindowManager(object):
    '''
    classdocs
    '''
    
    def __init__(self):
        self.rendered=dict()
        self.spacing = 14
        self.baseSize = 10
        self.scale = 10
        self.levelCounter = dict()
        self._display = DisplayFactory.getDisplayMechanism()
        self.spacing = self.scale * (self.spacing * 1.5) 
        self.baseSize = self.scale * self.baseSize
        '''
        Constructor
        '''
    
    def drawNode(self, level, node):
        
        print("Level :"+str(level))
        #if node is X make blue etc
        if level is 0:
            x_loc = 0
            y_loc = (level+1)*self.spacing
            width = self.baseSize * 1.5
            self.rendered[node] = self._display.drawSquare(x_loc, y_loc, width, self.baseSize, "#FFFF00", node.toString())
            self._display.drawTextInId(self.rendered[node], node.toShortString())
        else:
            if not self.isNodeRendered(node):
                if level not in self.levelCounter:
                    self.levelCounter[level] = 0
                else:
                    self.levelCounter[level] = self.levelCounter[level] + 1
                x_loc = self.levelCounter[level]*self.spacing
                y_loc = (level+1)*self.spacing
                width = self.baseSize * 1.5
                self.rendered[node] = self._display.drawCircle(x_loc, y_loc, width, self.baseSize, node.getType().value, node.toString())
                self._display.drawTextInId(self.rendered[node], node.toShortString())
    
    def connectNodes(self, master, slave):
        masterId = self.rendered.get(master)
        slaveId = self.rendered.get(slave)
        if masterId and slaveId:
            print(masterId)
            print(slaveId)
            # Needs to be associated with the node attached to
            lineval = self._display.connectIdWithLine(masterId, slaveId, slave.getType().value)
        else:
            print("Node values could not be extracted from render list, no joining will be done")        
        #could do with storing
    
    def isNodeRendered(self, node):
        if node in self.rendered:
            return True
        else:
            return False
        
    def finalise(self):
        self._display.runDisplay()
        pass