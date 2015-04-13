'''
Created on 31 Mar 2015

@author: WMOORHOU
'''

class Pom(object):
    '''
    classdocs
    '''

    def __init__(self, groupId, artifactId, version, fileLoc, parent=None, dependencies=None, modules=[]):
        self._groupId = groupId
        self._artifactId = artifactId
        self._version = version
        self._fileLoc = fileLoc
        self._parent = parent
        self._dependencies = dependencies
        self._modules = modules
        '''
        Constructor
        '''
    
    def getGroupId(self):
        if self._groupId == None:
            return ""
        else:
            return self._groupId
    
    def getArtifactId(self):
        return self._artifactId
    
    def getParentPom(self):
        return self._parent
        
    def getVersion(self):
        return self._version
    
    def getFileLocation(self):
        return self._fileLoc
    
    def getDependencies(self):
        return self._dependencies
    
    def getModules(self):
        return self._modules

    
class PomDependency(object):
    
    def __init__(self, groupId, artifactId, version):
        self._groupId = groupId
        self._artifactId = artifactId
        self._version = version
        
    def getGroupId(self):
        return self._groupId
    
    def getArtifactId(self):
        return self._artifactId
    
    def getVersion(self):
        return self._version    
    
    
