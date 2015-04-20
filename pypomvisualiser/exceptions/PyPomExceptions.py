'''
Created on 17 Apr 2015

@author: WMOORHOU
'''

class PomParseError(Exception):
    
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)