'''
Created on 31 Mar 2015

@author: WMOORHOU
'''
from src.display.TKWindowManager import WindowManager

class Visualiser(object):
    '''
    classdocs
    '''
    

    def __init__(self):
        self.manager = WindowManager()
        '''
        Constructor
        '''
    
    def visualisePomStructure(self, rootNode):
        ''' calculate number of nodes '''
        if rootNode:
            self.extractNodes(rootNode, 0)
    
        self.manager.finalise()
    
        ''' iterate over pom dependency structure'''
    def extractNodes(self, node, level):
        
        if level > 3:
            pass
        self.manager.drawNode(level, node)
        ''' node.get name etc render at this level'''
        
        print("child nodes: " + str(len(node.getChildNodes())))
        if len(node.getDependencies()) > 0:
            for dep in node.getDependencies():
                self.extractNodes(dep, level+1)
                self.manager.connectNodes(node, dep)
                pass
        
        if len(node.getChildNodes()) > 0:
            for child in node.getChildNodes():
                self.extractNodes(child, level+1)
                self.manager.connectNodes(node, child)
                
