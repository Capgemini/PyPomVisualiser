'''
Created on 30 Mar 2015

@author: WMOORHOU
'''
from src.ProjectActions import ProjectActions

def run():
    
    actions = ProjectActions()
    
    #actions.visualiseProject(r"D:\Users\wmoorhou\Documents\workspace")
    actions.visualiseProject(r"D:\Users\wmoorhou\Downloads\args4j-master")
    
    
    exit(1)
    
if __name__ == '__main__':
    run()