'''
Created on 31 Mar 2015

@author: WMOORHOU
'''
from ProjectScraper import ProjectScraper
from src.pom.PomParser import PomParser, TreeCreation
from src.display.Visualiser import Visualiser

class ProjectActions(object):
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''
        
    def visualiseProject(self, loc):
        
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
        visualise.visualisePomStructure(root)
        
        print("Finished gracefully")
        ''' Pass POPO structure to visualiser '''