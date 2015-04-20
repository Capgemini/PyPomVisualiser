'''
Created on 30 Mar 2015

@author: WMOORHOU
'''
from os import walk
from os import name
import logging

class ProjectScraper(object):
    
    '''
    classdocs
    platform specific detection
    '''
    def __init__(self):
        if name is "nt":
            self.__os_specific = r'\\'
        else:
            '''Not nt therefore likely to be posix'''
            self.__os_specific = r'/'
        logging.info("ProjectScraper: the OS type is " + name)
    '''
    Recursively find all poms in project
    '''
    def getProjectPomList(self, location):
        pomCollection = []
        for (dirpath, dirnames, filenames) in walk(location):
            if "pom.xml" in filenames:
                pomCollection.append(dirpath + self.__os_specific + "pom.xml")
            for tmpdir in dirnames:
                tmp = self.getProjectPomList(tmpdir)
                if tmp:
                    pomCollection.append(tmp)
        logging.info("ProjectScraper has found " + str(len(pomCollection)) + " poms.xml files.")
        return pomCollection
