'''
Created on 31 Mar 2015

@author: WMOORHOU
'''
from tkinter import Tk, Canvas, Scrollbar, Label, CURRENT, Button, Frame, Text
from src.display.DisplayTemplate import Display
from abc import abstractmethod

class TKinterDisplay(Display):
    '''
    classdocs
    '''
    
    
    '''
    Constructor
    '''
    def __init__(self, lineThickness=4):
        master = Tk()
        master.maxsize(1920, 1080)
        self.rendered = dict()
        self.currentlyRenderedWindow = None
        self.lineThickness = lineThickness
        self.local_canv = Canvas(master, width=400, height=400)
        self.vsb = Scrollbar(master, orient="vertical", command=self.local_canv.yview)
        self.local_canv.configure(yscrollcommand=self.vsb.set)
        self.hsb = Scrollbar(master, orient="horizontal", command=self.local_canv.xview)
        self.local_canv.configure(xscrollcommand=self.hsb.set)
        master.bind("<Configure>", self.OnFrameConfigure)
        self.hsb.pack(side="bottom", fill="x")
        self.vsb.pack(side="right", fill="y")
        self.local_canv.pack()
        self._sampleDraw()
        
        ''''''
    @abstractmethod    
    def drawSquare(self, x_loc, y_loc, width, height, colour=None, content=None):
        x2 = x_loc + width
        y2 = y_loc + height
        square = self.local_canv.create_rectangle(x_loc, y_loc, x2, y2, width=self.lineThickness, fill=colour, activeoutline="white")
        def handler(event, self=self, content=content):
                return self.onClick(event, content)
        self.local_canv.tag_bind(square, "<ButtonPress-1>", handler)
        return square
    
    @abstractmethod
    def drawCircle(self, x_loc, y_loc, width, height, colour=None, content=None):
        circle = self.local_canv.create_oval(x_loc, y_loc, x_loc + width, y_loc + height, width=self.lineThickness, fill=colour, activeoutline="white")
        
        def handler(event, self=self, content=content):
            return self.onClick(event, content)
        self.local_canv.tag_bind(circle, "<ButtonPress-1>", handler)
        return circle
    
    @abstractmethod
    def drawTextInId(self, componentId, content):
        id1tuple = self.getCoords(componentId)
        x1 = id1tuple[0] + ((id1tuple[2] - id1tuple[0])/2)
        y1 = id1tuple[1] + ((id1tuple[3] - id1tuple[1])/2)       
        return self.drawText(x1, y1, (id1tuple[2] - id1tuple[0]), content)
    
    def _sampleDraw(self):
        self.local_canv.create_oval(0, 0, 0, 0, width=0)
    
    def drawText(self, x, y, width, content):
        val = self.local_canv.create_text(x, y, width=width, text=content, justify="center", font="Helvetica 12 bold", anchor="center")
        self.local_canv.tag_raise(val)
        return val
    
    @abstractmethod
    def drawLine(self, x1, y1, x2, y2, colour="black"):
        line = self.local_canv.create_line(x1, y1, x2, y2, width=self.lineThickness, arrow="first", fill=colour)
        self.local_canv.tag_lower(line)
        return #line
    
    def connectIdWithLine(self, id1, id2, colour=None):
        id1tuple = self.getCoords(id1)
        x1 = id1tuple[0] + ((id1tuple[2] - id1tuple[0])/2)
        y1 = id1tuple[1] + ((id1tuple[3] - id1tuple[1])/2)
        id2tuple = self.getCoords(id2)
        x2 = id2tuple[0] + ((id2tuple[2] - id2tuple[0])/2)
        y2 = id2tuple[1] + ((id2tuple[3] - id2tuple[1])/2)
        return self.drawLine(x1, y1, x2, y2, colour)
    
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
    
    def onClick(self, event, content):
        self.createWindowOnId(self.local_canv.find_withtag(CURRENT), content)
    
    def onClickRemove(self, event):
        print("remove")
        self.remove(CURRENT)
        
    def createWindowOnId(self, itemId, content):
        self.remove(self.currentlyRenderedWindow)
        idtuple = self.local_canv.coords(itemId)
        if idtuple:
            x = idtuple[0]
            y = idtuple[1]
            frm = Frame(self.local_canv)
            #yScroll = Scrollbar(frm, orient="vertical", command=frm.yview)
            #yScroll.grid(row=0, column=1)
            frm.grid(row=0, column=0)
            Label(frm, text=content, background="#CCFFCC", borderwidth=6, relief="ridge", justify="left").grid(row=0,column=0)
            
            self.currentlyRenderedWindow = self.local_canv.create_window(x, y, window=frm)
            localId = self.currentlyRenderedWindow
            Button(frm, text="Close", command= lambda :  self.remove(localId)).grid(row=4,column=0)
            