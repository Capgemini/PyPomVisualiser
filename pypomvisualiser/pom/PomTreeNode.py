'''
Created on 10 Apr 2015

@author: WMOORHOU
'''
class PomTreeNode(object):

    def __init__(self, artId, groupId, nodeType, data):
        self.artifactId = artId
        self.groupId = groupId
        self.parentNode = None
        self.dependencyNodes = []
        self._reverseDependencies = []
        self.childnodes = []
        if len(self.childnodes) != 0:
            raise Exception
        self.data = data
        self.type = nodeType
    
    def getGroupId(self):
        return self.groupId
    
    def getArtifactId(self):
        return self.artifactId

    def setData(self, data):
        self.data = data
    
    def getData(self):
        return self.data
    
    def getParent(self):
        return self.parentNode
    
    def setParentNode(self, thisnode):
        assert type(thisnode) is PomTreeNode
        self.parentNode = thisnode

    def getType(self):
        return self.type
    
    def setType(self, nodeType):
        self.type = nodeType

    # reverse parent idea
    def addChildNodes(self, node):
        if node not in self.childnodes:
            self.childnodes.append(node)
            pass
        
    def getChildNodes(self):
        return self.childnodes
    
    def getDependencies(self):
        return self.dependencyNodes
    
    def addDependencyNode(self, node):
        assert type(node) is PomTreeNode
        if node not in self.dependencyNodes:
            self.dependencyNodes.append(node)
    
    def getReverseDependencyNodes(self):
        return self._reverseDependencies
    
    def addReverseDependencyNode(self, node):
        assert type(node) is PomTreeNode
        if node not in self._reverseDependencies:
            self._reverseDependencies.append(node)

    def toShortString(self):
        output = "artifact: " + (self.artifactId if not None else "Empty") + "\n"
        output += "group: " + (self.groupId if not None else "Empty") + "\n"
        data = self.getData()
        if data != None:
            data = data.getVersion()
            if data != None:
                output += "version: " + (data if not None else "Empty") + "\n"
        return output

    def toString(self):
        output = ""
        if self.getGroupId():
            output = "GroupId: " + self.getGroupId() + "\n"
        if self.getArtifactId():
            output += "ArtifactId: " + self.getArtifactId() +"\n"
        if self.getData():
            data = self.getData()
            if data.getVersion():
                output += "Version: " + data.getVersion() + "\n" 
        if self.getParent():
            output += "\nParent:  \n"
            if self.getParent().getGroupId() != None:
                output += "    parent groupId: " + self.parentNode.getGroupId() + "\n"
            if self.parentNode.getArtifactId() != None:
                output += "    parent artifactId: " + self.parentNode.getArtifactId() + "\n"
        
        output += "\nDependencies: \n"
        for dep in self.getDependencies():
            output += "    dependency: \n"
            if dep.getGroupId():
                output += "        GroupID: " + dep.getGroupId() + "\n"
            if dep.getArtifactId():
                output += "        ArtifactId: " + dep.getArtifactId() + "\n"
            if dep.getData():
                if dep.getData().getVersion():
                    output += "Version: " + dep.getData().getVersion() + "\n" 
        
        output += "\nDependent on this pom: \n"   
        for dep in self.getReverseDependencyNodes():
            output += "    Reverse dependency: \n"
            if dep.getGroupId():
                output += "        GroupId: " + dep.getGroupId() + "\n"
            if dep.getArtifactId():
                output += "        ArtifactId: " + dep.getArtifactId() + "\n"
            if dep.getData():
                if dep.getData().getVersion():
                    output += "Version: " + dep.getData().getVersion() + "\n"
        
        output += "\nParent to: \n"   
        for dep in self.getChildNodes():
            output += "    Child: \n"
            if dep.getGroupId():
                output += "        GroupId: " + dep.getGroupId() + "\n"
            if dep.getArtifactId():
                output += "        ArtifactId: " + dep.getArtifactId() + "\n"
            if dep.getData():
                if dep.getData().getVersion():
                    output += "Version: " + dep.getData().getVersion() + "\n"
        return output 
