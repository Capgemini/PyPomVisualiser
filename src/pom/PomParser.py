'''
Created on 31 Mar 2015

@author: WMOORHOU
'''

from xml.dom.minidom import parse
from src.pom.Pom import PomDependency, Pom
from src.pom.PomTreeNode import PomTreeNode
from enum import Enum
from test.test_tarfile import tmpname

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
        try:
            for file in listOfFileLocs:
                current = file
                tmpDom = parse(file)
                if tmpDom:
                    self.popos.append(self.DomToPOPO(tmpDom, file))
                    tmpDom.unlink()
            return self.popos   
        except Exception:
            raise PomParseError("Parser was unable to parse from file location: " + current)
            
    
    def DomToPOPO(self, dom, file):
        pomDeps = []
        parent = None
        par = dom.getElementsByTagName("parent")
        if par:
            par = par[0]
            grp = self.getNodeValue(par.getElementsByTagName("groupId"))
            art = self.getNodeValue(par.getElementsByTagName("artifactId"))
            ver = self.getNodeValue(par.getElementsByTagName("version"))
            relPath = self.getNodeValue(par.getElementsByTagName("relativePath"))
            parent = Pom(grp, art, ver, relPath)
                
        pomGrp = self.getNodeValue(dom.getElementsByTagName("groupId"))
        pomArt = self.getNodeValue(dom.getElementsByTagName("artifactId"))
        pomVer = self.getNodeValue(dom.getElementsByTagName("version"))
        
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
                    
            '''        
            parentPom = pom.getParentPom()
            if parentPom != None:
                grpId = parentPom.getGroupId()
                artId = parentPom.getArtifactId()
                parentPom1 = self.getNodeWith(artId, grpId)
                if parentPom1 != None:
                    tmpnode.setParentNode(parentPom1)
                else:
                    parentPom1 = PomTreeNode(artId, grpId, NodeEnum.USERPOM, None)
                    self.nodeList.append(parentPom1)
                    tmpnode.setParentNode(parentPom1)
            '''        
                    
            '''determines if pom has parent, if it does, determine if in nodeList and add as parentNode '''
            if pom.getParentPom():
                parPom = pom.getParentPom()
                par = self.inNodeList(self.nodeList, PomTreeNode(parPom.getArtifactId(), parPom.getGroupId(), NodeEnum.USERPOM, None))
                tmpnode.setParentNode(par)
                par.addChildNodes(tmpnode)
            '''#################### '''
                
            
            ''' determine if any nodes match the dependencies and then add dep nodes accordingly'''
            for dep in pom.getDependencies():
                notfound = True
                for inner in listOfPoms:
                    if (inner.getGroupId() == dep.getGroupId()) and (inner.getArtifactId() == dep.getArtifactId()):                        
                        ''' inner is dependency, make node which refers to this.'''
                        foundNode = self.inNodeList(self.nodeList, PomTreeNode(inner.getArtifactId, inner.getGroupId(), NodeEnum.USERPOM, None)) 
                        tmpnode.addDependencyNode(foundNode)
                        foundNode.addReverseDependencyNode(tmpnode)
                        notfound = False
                        break
                # Add reverse dependency assignment
                if notfound is True:
                    depNode = self.inNodeList(self.nodeList, PomTreeNode(dep.getArtifactId(), dep.getGroupId(), NodeEnum.EXTDEP, None))
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
        if parent != None:
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
