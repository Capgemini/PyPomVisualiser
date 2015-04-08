'''
Created on 31 Mar 2015

@author: WMOORHOU
'''
from tkinter import Tk, Canvas
from src.display.OutDisplay import OutDisplay

class Win32Display(OutDisplay):
    '''
    classdocs
    '''
    window = None
    
    '''
    Constructor
    '''
    def __init__(self):
        master = Tk()
        self.window = Canvas(master, width=150, height=150)
        self.window.pack()
        ''''''
        
    def drawSquare(self, x_loc, y_loc, width, height):
        x2 = x_loc + width
        y2 = y_loc + height
        print("SQUARE")
        return self.window.create_rectangle(x_loc, y_loc, x2, y2)
    
    def drawCircle(self, x_loc, y_loc, width, height):
        print("circle")
        return self.window.create_oval(x_loc, y_loc, width, height)
    
    def remove(self, num):
        self.window.delete(num)
    
    def runDisplay(self):
        self.window.mainloop()