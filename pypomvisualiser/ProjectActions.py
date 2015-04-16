'''
Created on 31 Mar 2015

@author: WMOORHOU
'''
from pypomvisualiser.ProjectScraper import ProjectScraper
from pypomvisualiser.pom.PomParser import PomParser, TreeCreation
from pypomvisualiser.display.Visualiser import Visualiser

class ProjectActions(object):
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''
    @staticmethod
    def visualiseProject(loc):
        
        ''' Get poms in project'''
        scraper = ProjectScraper()
        pomLocs = scraper.getProjectPomList(loc)
        
        ''' Parse XML into some Pom POPOs'''
        pomparser = PomParser()
        pomPOPOs = pomparser.parseFilesToPomPOPO(pomLocs)
        ''' Process POPOs to determine dependencies '''
        
        ''' Create POPO structure '''
        root = TreeCreation(pomPOPOs).getRootNode()
        
        print(root)
        
        visualise = Visualiser()
        ''' Pass POPO structure to visualiser '''
        visualise.visualisePomStructure(root)
        
        print("Finished gracefully")