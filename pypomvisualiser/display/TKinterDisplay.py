'''
Created on 31 Mar 2015

@author: WMOORHOU
'''
from tkinter import Tk, Canvas, Scrollbar, Label, CURRENT, Button, Frame, N, S
from pypomvisualiser.display.DisplayTemplate import Display
from abc import abstractmethod
import logging
import math

class TKinterDisplay(Display):
    '''
    classdocs
    '''
    
    
    '''
    Constructor
    '''
    def __init__(self, lineThickness=3, maxH=1920, maxW=1080):
        master = Tk()
        master.maxsize(maxH, maxW)
        self.localCanvas = Canvas(master, width=400, height=400)
        
        self.currentlyRenderedWindow = None
        self.lineThickness = lineThickness
        
        self.vsb = Scrollbar(master, orient="vertical", command=self.localCanvas.yview)
        self.hsb = Scrollbar(master, orient="horizontal", command=self.localCanvas.xview)
        
        self.localCanvas.configure(yscrollcommand=self.vsb.set)
        self.localCanvas.configure(xscrollcommand=self.hsb.set)
        
        master.bind("<Configure>", self.__eventOnFrameConfigure)
        self.hsb.pack(side="bottom", fill="x")
        self.vsb.pack(side="right", fill="y")
        self.localCanvas.pack()
        self.__sampleDraw()
        
        ''''''
    @abstractmethod    
    def drawSquare(self, xywhTuple, tags=None, colour=None, content=None):
        x2 = xywhTuple[0] + xywhTuple[2]
        y2 = xywhTuple[1] + xywhTuple[3]
        square = self.localCanvas.create_rectangle(xywhTuple[0], xywhTuple[1], x2, y2, width=self.lineThickness, tags=tags, fill=colour, activeoutline="white")
        def handler(event, self=self, content=content):
                return self.__eventOnClick(event, content)
        self.localCanvas.tag_bind(square, "<ButtonRelease-1>", handler)
        return square
    
    @abstractmethod
    def drawCircle(self, xywhTuple, tags=None , colour=None, content=None):
        x2 = xywhTuple[0] + xywhTuple[2]
        y2 = xywhTuple[1] + xywhTuple[3]
        circle = self.localCanvas.create_oval(xywhTuple[0], xywhTuple[1], x2, y2, width=self.lineThickness, tags=tags, fill=colour, activeoutline="white")
        
        def handler(event, self=self, content=content):
            return self.__eventOnClick(event, content)
        self.localCanvas.tag_bind(circle, "<ButtonRelease-1>", handler)
        return circle
    
    @abstractmethod
    def connectIdWithLine(self, id1, id2, tags=None, colour=None):
        
        # Gets the coordinates of id1 and then calulates centre point
        id1tuple = self.__getCoords(id1)
        x1 = id1tuple[0] + ((id1tuple[2] - id1tuple[0]) / 2)
        y1 = id1tuple[1] + ((id1tuple[3] - id1tuple[1]) / 2)
        
        # Gets the coordinates of id2 and then calulates centre point
        id2tuple = self.__getCoords(id2)
        x2 = id2tuple[0] + ((id2tuple[2] - id2tuple[0]) / 2)
        y2 = id2tuple[1] + ((id2tuple[3] - id2tuple[1]) / 2)
        
        # Calculates, using trig, the angle of the line at shape id1. This gives the radius of the ellipse
        opposite = y1 - y2
        adjacent = x1 - x2
        x1angle = 0
        x2angle = 0
        hyp = 0
        if adjacent != 0 and opposite != 0:
            hyp = math.sqrt(math.pow(opposite, 2) + math.pow(adjacent, 2))
            x1angle = math.tan(opposite / adjacent)
            x2angle = math.tan(adjacent / opposite)           
        else:
            
            if opposite == 0:
                hyp = adjacent
            else:
                hyp = opposite    
            x1angle = math.radians(90)
            x2angle = math.radians(270)
        
        a1 = (id1tuple[2] - id1tuple[0]) / 2
        b1 = (id1tuple[3] - id1tuple[1]) / 2
        
        a2 = (id2tuple[2] - id2tuple[0]) / 2
        b2 = (id2tuple[3] - id2tuple[1]) / 2
        
        r1 = a1 * b1 / (math.sqrt(((a1 * a1) * (math.pow(math.sin(x1angle), 2))) + ((b1 * b1) * math.pow(math.cos(x1angle), 2))))
        r2 = a2 * b2 / (math.sqrt(((a2 * a2) * (math.pow(math.sin(x2angle), 2))) + ((b2 * b2) * math.pow(math.cos(x2angle), 2))))
        
        x1 = x1 + ((r1 / hyp) * (x2 - x1))
        y1 = y1 + ((r1 / hyp) * (y2 - y1))
        
        #x2 = x2 + ((r2 / hyp) * (x1 - x2))
        #y2 = y2 - ((r2 / hyp) * (y1 - y2))
                    
        return self.__drawLine(x1, y1, x2, y2, tags, colour)
    
    @abstractmethod
    def renderTextInId(self, tagTocentreOn, tagsToAddTo, content, funcContent):
        id1tuple = self.__getCoords(tagTocentreOn)
        x1 = id1tuple[0] + ((id1tuple[2] - id1tuple[0]) / 2)
        y1 = id1tuple[1] + ((id1tuple[3] - id1tuple[1]) / 2)       
        txt = self.__renderText(x1, y1, (id1tuple[2] - id1tuple[0]), content, tagsToAddTo)
        
        def handler(event, self=self, content=funcContent):
            return self.__eventOnClick(event, content)
        
        self.localCanvas.tag_bind(txt, "<ButtonRelease-1>", handler)
        return txt
    
    @abstractmethod
    def move(self, tag, xamount, yamount):
        self.localCanvas.move(tag, xamount, yamount)

    @abstractmethod    
    def runDisplay(self):
        self.localCanvas.mainloop()
    
    
    def __hideId(self, objectId):
        self.localCanvas.itemconfigure(objectId, state="hidden")
        pass
        
    def __showId(self, objectId):
        self.localCanvas.itemconfigure(objectId, state="normal")
        pass
    
    def __sampleDraw(self):
        self.localCanvas.create_oval(0, 0, 0, 0, width=0)
    
    def __renderText(self, x, y, width, content, tag):
        val = self.localCanvas.create_text(x, y, width=width, text=content, tags=tag, justify="center", font="Helvetica 8 bold", anchor="center")
        self.localCanvas.tag_raise(val)
        return val
    
    def __drawLine(self, x1, y1, x2, y2, tags=None, colour="black"):
        line = self.localCanvas.create_line(x1, y1, x2, y2, tags=tags, width=self.lineThickness, arrow="first", arrowshape=(16,20,6),fill=colour, smooth=True)
        self.localCanvas.tag_lower(line)
        return  # line
    
    def __remove(self, num):
        self.localCanvas.delete(num)
    
    def __getCoords(self, ident):
        return self.localCanvas.coords(ident)
    
    def __eventOnFrameConfigure(self, event):
        '''Reset the scroll region to encompass the inner frame'''
        assert self.localCanvas
        coord_tuple = self.localCanvas.bbox("all")
        if not coord_tuple:
            logging.error("Frame reconfigure error on coordinate acquire.")
        else:
            reconWidth = coord_tuple[2] - coord_tuple[0]
            reconHeight = coord_tuple[3] - coord_tuple[1]
            self.localCanvas.configure(width=reconWidth)
            self.localCanvas.configure(height=reconHeight)
            self.localCanvas.configure(scrollregion=self.localCanvas.bbox("all"))
            self.localCanvas.update_idletasks()
    
    def __eventOnClick(self, event, content):
        self.__createWindowOnId(self.localCanvas.find_withtag(CURRENT), content)
        
    def __createWindowOnId(self, itemId, content):
        if self.currentlyRenderedWindow != None:
            self.currentlyRenderedWindow()
        # self.__remove(self.currentlyRenderedWindow)
        idtuple = self.localCanvas.coords(itemId)
        if idtuple:
            x = idtuple[0]
            y = idtuple[1]
            frm = Frame(self.localCanvas)
            frm.grid(row=0, column=0)
            canv = Canvas(frm)            
            
            vscroll = Scrollbar(frm, orient="vertical", command=canv.yview)
            vscroll.grid(row=0, column=1, sticky=N + S)
            
            canv.grid(row=0, column=0)
            
            canv["yscrollcommand"] = vscroll.set
            aframe = Frame(canv)
            aframe.grid(row=0, column=0)
            Label(aframe, text=content, anchor="center", background="#CCFFCC", borderwidth=6, relief="ridge", justify="left").grid(row=1, column=0)
            canvWindow = canv.create_window(x, y, window=aframe)
            canv.coords(canvWindow, x, y)
            self.localCanvas.update_idletasks()
            canv["scrollregion"] = canv.bbox("all")
            
            def destroyAll():
                self.__remove(canvWindow)
                canv.destroy()
                aframe.destroy()
                vscroll.destroy()
                frm.destroy()
                
            self.currentlyRenderedWindow = destroyAll 
            Button(frm, text="Close", command=lambda :  destroyAll()).grid(row=2, column=0)
