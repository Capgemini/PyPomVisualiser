'''
Created on 31 Mar 2015

@author: WMOORHOU
'''
from tkinter import Tk, Canvas, Scrollbar
from src.display.DisplayFactory import Display
from abc import abstractmethod

class Win32Display(Display):
    '''
    classdocs
    '''
    local_canv = None
    
    '''
    Constructor
    '''
    def __init__(self, lineThickness=3):
        master = Tk()
        self.lineThickness = lineThickness
        self.local_canv = Canvas(master, width=400, height=400)
        self.vsb = Scrollbar(master, orient="vertical", command=self.local_canv.yview)
        self.local_canv.configure(yscrollcommand=self.vsb.set)
        master.bind("<Configure>", self.OnFrameConfigure)
        self.vsb.pack(side="right", fill="y")
        self.local_canv.pack()
        self._sampleDraw()
        ''''''
    @abstractmethod    
    def drawSquare(self, x_loc, y_loc, width, height):
        x2 = x_loc + width
        y2 = y_loc + height
        print("SQUARE")
        return self.local_canv.create_rectangle(x_loc, y_loc, x2, y2, width=self.lineThickness)
    
    @abstractmethod
    def drawCircle(self, x_loc, y_loc, width, height, function=None):
        if not function:
            print("circle")
            return self.local_canv.create_oval(x_loc, y_loc, x_loc + width, y_loc + height, width=self.lineThickness)
        else:
            circle = self.local_canv.create_oval(x_loc, y_loc, x_loc + width, y_loc + height, width=self.lineThickness)
            # self.local_canv.tag_bind(circle, "", function)
            return circle
    
    def _sampleDraw(self):
        self.local_canv.create_oval(0, 0, 0, 0, width=0)
    
    @abstractmethod
    def drawLine(self, x1, y1, x2, y2):
        print("Drawing line")
        line = self.local_canv.create_line(x1, y1, x2, y2, width=self.lineThickness)
        self.local_canv.tag_lower(line)
        return line
    
    def connectIdWithLine(self, id1, id2):
        id1tuple = self.getCoords(id1)
        x1 = id1tuple[0] + ((id1tuple[2] - id1tuple[0])/2)
        y1 = id1tuple[1] + ((id1tuple[3] - id1tuple[1])/2)
        id2tuple = self.getCoords(id2)
        x2 = id2tuple[0] + ((id2tuple[2] - id2tuple[0])/2)
        y2 = id2tuple[1] + ((id2tuple[3] - id2tuple[1])/2)
        print("x1 " + str(x1))
        print("y1 " + str(y1))
        print("x2 " + str(x2))
        print("y2 " + str(y2))
        
        return self.drawLine(x1, y1, x2, y2)
    
    @abstractmethod
    def remove(self, num):
        self.local_canv.delete(num)

    @abstractmethod    
    def runDisplay(self):
        self.local_canv.mainloop()
    
    def getCoords(self, ident):
        return self.local_canv.coords(ident)
    
        
    def OnFrameConfigure(self, event):
        '''Reset the scroll region to encompass the inner frame'''
        
        assert self.local_canv
        
        coord_tuple = self.local_canv.bbox("all")
        
        if not coord_tuple:
            print("Something horrible happened")
        else:
            reconWidth = coord_tuple[2] - coord_tuple[0]
            reconHeight = coord_tuple[3] - coord_tuple[1]
            self.local_canv.configure(width=reconWidth)
            self.local_canv.configure(height=reconHeight)
            self.local_canv.configure(scrollregion=self.local_canv.bbox("all"))
            
        
    
