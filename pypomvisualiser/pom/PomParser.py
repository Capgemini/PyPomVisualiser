'''
Created on 31 Mar 2015

@author: WMOORHOU
'''

from xml.dom.minidom import parse
from pypomvisualiser.pom.Pom import Pom, PomDependency
from pypomvisualiser.exceptions.PyPomExceptions import PomParseError

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
        
