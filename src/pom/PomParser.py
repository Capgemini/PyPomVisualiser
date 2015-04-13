'''
Created on 31 Mar 2015

@author: WMOORHOU
'''

from xml.dom.minidom import parse
from src.pom.Pom import PomDependency, Pom
from src.pom.PomTreeNode import PomTreeNode
from enum import Enum
import xml.etree.ElementTree as ET

class PomParser(object):
    '''
    classdocs
    '''
    def __init__(self):
        self.popos = []
        self.current = None
        '''
        Constructor
        '''
        
    def parseFilesToPomPOPO(self, listOfFileLocs):
        #try:
            for file in listOfFileLocs:
                current = file
                tmpDom = parse(file)
                if tmpDom:
                    self.popos.append(self.DomToPOPO(tmpDom, file))
                    tmpDom.unlink()
            return self.popos   
        #except Exception:
            #raise PomParseError("Parser was unable to parse from file location: " + current)
    
    def DomToPOPO(self, dom, file):
        pomDeps = []
        parent = None
        par = dom.getElementsByTagName("parent")
        if par:
            grp = None
            art = None
            ver = None
            relPath = None
            for child in par[0].childNodes:
                local = child.localName
                if local == "groupId":
                    grp = child.firstChild.nodeValue
                elif local == "artifactId":
                    art = child.firstChild.nodeValue
                elif local == "version":
                    ver = child.firstChild.nodeValue
                elif local == "relativePath":
                    relPath = child.firstChild.nodeValue
            parent = Pom(grp, art, ver, relPath)
        
        pomGrp = None
        pomArt = None
        pomVer = None
        
        for child in dom.getElementsByTagName("project")[0].childNodes:
            local = child.localName
            if local == "groupId":
                pomGrp = child.firstChild.nodeValue
            elif local == "artifactId":
                pomArt = child.firstChild.nodeValue
            elif local == "version":
                pomVer = child.firstChild.nodeValue
        
        depMan = dom.getElementsByTagName("dependencyManagement")
        if depMan:
            deps = depMan.getElementsByTagName("dependencies")
        else:
            deps = dom.getElementsByTagName("dependencies")
        
        for no in deps:
            tmps = no.getElementsByTagName("dependency")
            for dep in tmps:
                if dep:
                    depGrp = self.getNodeValue(dep.getElementsByTagName("groupId"))
                    depArt = self.getNodeValue(dep.getElementsByTagName("artifactId"))
                    depVer = self.getNodeValue(dep.getElementsByTagName("version"))
                    pomDeps.append(PomDependency(depGrp, depArt, depVer))
            
        mods = dom.getElementsByTagName("modules")
        pomMods = []
        for mod in mods:
            pomMods.append(self.getNodeValue(mod.getElementsByTagName("module")))
            
        return Pom(pomGrp, pomArt, pomVer, file, parent, pomDeps, pomMods)
    
    def getNodeValue(self, elementByTag):
        if elementByTag:
            if len(elementByTag) > 0:
                elementByTag = elementByTag[0]
                if len(elementByTag.childNodes) > 0:
                    elementByTag = elementByTag.childNodes[0]
                    return elementByTag.nodeValue
        
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
            
            print (pomArt)
            print (pomGrp)
            
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
                    #par = self.getNodeWith(parPom.getArtifactId, parPom.getGroupId) if not None else PomTreeNode(parPom.getArtifactId(), parPom.getGroupId(), NodeEnum.USERPOM, None)
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
                    depNode = self.inNodeList(self.nodeList, PomTreeNode(dep.getArtifactId(), dep.getGroupId(), NodeEnum.EXTDEP, None))
                    
                    # Something causing None or bad type to be thrown into setter
                    
                    print("artid "  + depNode.getArtifactId())
                    
                    tmpnode.addDependencyNode(depNode)
                    depNode.addReverseDependencyNode(tmpnode)
                    pass
                
            ''' ################### '''
            #self.nodeList.append(tmpnode)
        self.resolveRootNode()
        ''' Count number of layers maybe?'''
    
    def getNodeWith(self,artId, grpId):
        
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
            if length is not 1:
                ''' more than 1 node'''
                active = self.nodeList[0]
                assert type(active) is PomTreeNode
                # May need more work
                self.resolveNodeRelations(active)
            else:
                self.rootNode = self.nodeList[0]
                return                
        else:
            ''' throw exception'''
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
            print("Root node chosen: " + potentialRootNode.getArtifactId() + " " + potentialRootNode.getGroupId())
            
            ''' Could be root node'''
            
    def getRootNode(self):
        return self.rootNode    

class NodeEnum(Enum):
    EXTDEP = "green"
    USERPOM = "#0080FF"

class PomParseError(Exception):
    
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)
