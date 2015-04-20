from pypomvisualiser.pom.PomTreeNode import PomTreeNode
from pypomvisualiser.exceptions.PyPomExceptions import PomParseError
from enum import Enum
import logging

class NodeEnum(Enum):
    EXTDEP = "#C0C0C0"
    USERPOM = "#99CCFF"
    ROOTPOM = "#0099FF"


class TreeCreation(object):
    
    def __init__(self, listOfPoms):
        ''' '''
        self.rootNode = None
        self.nodeList = []
        self.resolveTreeStructure(listOfPoms)
                
    def resolveTreeStructure(self, listOfPoms):
        for pom in listOfPoms:
            print(pom.getFileLocation())
            pomArt = pom.getArtifactId()
            pomGrp = pom.getGroupId()
            ''' If node is in found list then use that, if not make a new one'''
            tmpnode = self.getNodeWith(pomArt, pomGrp)
            if tmpnode == None:
                tmpnode = PomTreeNode(pomArt, pomGrp, NodeEnum.USERPOM, pom)
                self.nodeList.append(tmpnode)
            if tmpnode.getData() == None:
                tmpnode.setData(pom)
            ''' ####################'''
                    
            '''determines if pom has parent, if it does, determine if in nodeList and add as parentNode'''
            if pom.getParentPom():
                parPom = pom.getParentPom()
                if (pomArt == parPom.getArtifactId) and (pomGrp == parPom.getGroupId):
                    pass
                else:
                    par = self.inNodeList(self.nodeList, PomTreeNode(parPom.getArtifactId(), parPom.getGroupId(), NodeEnum.USERPOM, None)) 
                    tmpnode.setParentNode(par)
                    par.addChildNodes(tmpnode)
            
            ''' determine if any nodes match the dependencies and then add dep nodes accordingly'''
            for dep in pom.getDependencies():
                notfound = True
                for inner in listOfPoms:
                    if (inner.getGroupId() == dep.getGroupId()) and (inner.getArtifactId() == dep.getArtifactId()):                        
                        ''' inner is dependency, make node which refers to this.'''
                        foundNode = self.inNodeList(self.nodeList, PomTreeNode(inner.getArtifactId(), inner.getGroupId(), NodeEnum.USERPOM, None)) 
                        tmpnode.addDependencyNode(foundNode)
                        foundNode.addReverseDependencyNode(tmpnode)
                        notfound = False
                        break
                # Add reverse dependency assignment
                if notfound is True:
                    depNode = self.inNodeList(self.nodeList, PomTreeNode(dep.getArtifactId(), dep.getGroupId(), NodeEnum.EXTDEP, dep))
                    tmpnode.addDependencyNode(depNode)
                    depNode.addReverseDependencyNode(tmpnode)
            ''' ################### '''
        self.resolveRootNode()
    
    def getNodeWith(self, artId, grpId):
        
        for temporaryNode in self.nodeList:
            if (temporaryNode.getGroupId() == grpId) and (temporaryNode.getArtifactId() == artId):
                return temporaryNode
    
    
    def inNodeList(self, nodeList, nodeToFind):
        assert type(nodeToFind) is PomTreeNode
        for node in nodeList:
            if (node.getGroupId() == nodeToFind.getGroupId()) and (node.getArtifactId() == nodeToFind.getArtifactId()):
                self.nodeList.append(node)
                return node
        self.nodeList.append(nodeToFind)
        return nodeToFind
    
    def resolveRootNode(self):
        length = len(self.nodeList)
        
        if length > 0:
            activeNode = None
            for node in self.nodeList:
                assert type(node) is PomTreeNode
                if activeNode != None:
                    act = self.resolveNodeRelations(node)
                    if act != activeNode:
                        logging.error("Multiple root nodes encountered")
                        raise PomParseError("Resolution of RootNode failed as the structure contains multiple trees")
                else:
                    activeNode = self.resolveNodeRelations(node)
        else:
            raise PomParseError("Resolution of RootNode failed as the structure is empty")
    
    def resolveNodeRelations(self, potentialRootNode):
        
        parent = potentialRootNode.getParent()
        if parent != None and parent != potentialRootNode:
            print(parent.getArtifactId())
            self.resolveNodeRelations(parent)
        elif potentialRootNode.getReverseDependencyNodes():
            print("rev dep nodes")
            ''' Needs to follow these, maybe one, maybe all'''
        else:
            self.rootNode = potentialRootNode
            logging.info("Root node chosen: " + potentialRootNode.getArtifactId() + " " + potentialRootNode.getGroupId())
            self.rootNode.setType(NodeEnum.ROOTPOM)
            ''' Could be root node'''
            
    def getRootNode(self):
        return self.rootNode