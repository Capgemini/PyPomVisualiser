'''
Created on 31 Mar 2015

@author: WMOORHOU
'''
from tkinter import Tk, Canvas, Scrollbar, Label, CURRENT, Button, Frame, N, S
from pypomvisualiser.display.DisplayTemplate import Display
from abc import abstractmethod

class TKinterDisplay(Display):
    '''
    classdocs
    '''
    
    
    '''
    Constructor
    '''
    def __init__(self, lineThickness=3):
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
    def drawSquare(self, xywhTuple, tags=None, colour=None, content=None):
        x2 = xywhTuple[0] + xywhTuple[2]
        y2 = xywhTuple[1] + xywhTuple[3]
        square = self.local_canv.create_rectangle(xywhTuple[0], xywhTuple[1], x2, y2, width=self.lineThickness, tags=tags, fill=colour, activeoutline="white")
        def handler(event, self=self, content=content):
                return self.onClick(event, content)
        self.local_canv.tag_bind(square, "<ButtonRelease-1>", handler)
        return square
    
    @abstractmethod
    def drawCircle(self, xywhTuple, tags=None , colour=None, content=None):
        x2 = xywhTuple[0] + xywhTuple[2]
        y2 = xywhTuple[1] + xywhTuple[3]
        circle = self.local_canv.create_oval(xywhTuple[0], xywhTuple[1], x2, y2, width=self.lineThickness, tags=tags, fill=colour, activeoutline="white")
        
        def handler(event, self=self, content=content):
            return self.onClick(event, content)
        self.local_canv.tag_bind(circle, "<ButtonRelease-1>", handler)
        return circle
    
    @abstractmethod
    def drawTextInId(self, tagTocentreOn, tagsToAddTo, content, funcContent):
        id1tuple = self.getCoords(tagTocentreOn)
        x1 = id1tuple[0] + ((id1tuple[2] - id1tuple[0]) / 2)
        y1 = id1tuple[1] + ((id1tuple[3] - id1tuple[1]) / 2)       
        txt = self.drawText(x1, y1, (id1tuple[2] - id1tuple[0]), content, tagsToAddTo)
        
        def handler(event, self=self, content=funcContent):
            return self.onClick(event, content)
        
        self.local_canv.tag_bind(txt, "<ButtonRelease-1>", handler)
        return txt
    
    def hideId(self, objectId):
        self.local_canv.itemconfigure(objectId, state="hidden")
        pass
        
    def showId(self, objectId):
        self.local_canv.itemconfigure(objectId, state="normal")
        pass
    
    def _sampleDraw(self):
        self.local_canv.create_oval(0, 0, 0, 0, width=0)
    
    def drawText(self, x, y, width, content, tag):
        val = self.local_canv.create_text(x, y, width=width, text=content, tags=tag, justify="center", font="Helvetica 12 bold", anchor="center")
        self.local_canv.tag_raise(val)
        return val
    
    @abstractmethod
    def drawLine(self, x1, y1, x2, y2, tags=None, colour="black"):
        line = self.local_canv.create_line(x1, y1, x2, y2, tags=tags, width=self.lineThickness, arrow="first", fill=colour)
        self.local_canv.tag_lower(line)
        return  # line
    
    def connectIdWithLine(self, id1, id2, tags=None, colour=None):
        id1tuple = self.getCoords(id1)
        x1 = id1tuple[0] + ((id1tuple[2] - id1tuple[0]) / 2)
        y1 = id1tuple[1] + ((id1tuple[3] - id1tuple[1]) / 2)
        id2tuple = self.getCoords(id2)
        x2 = id2tuple[0] + ((id2tuple[2] - id2tuple[0]) / 2)
        y2 = id2tuple[1] + ((id2tuple[3] - id2tuple[1]) / 2)
        return self.drawLine(x1, y1, x2, y2, tags, colour)
    
    @abstractmethod
    def remove(self, num):
        self.local_canv.delete(num)

    @abstractmethod    
    def runDisplay(self):
        self.local_canv.mainloop()
    
    def move(self, tag, xamount, yamount):
        self.local_canv.move(tag, xamount, yamount)
    
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
            self.local_canv.update_idletasks()
    
    def onClick(self, event, content):
        self.createWindowOnId(self.local_canv.find_withtag(CURRENT), content)
    
    def onClickRemove(self, event):
        print("remove")
        self.remove(CURRENT)
        
    def createWindowOnId(self, itemId, content):
        if self.currentlyRenderedWindow != None:
            self.currentlyRenderedWindow()
        # self.remove(self.currentlyRenderedWindow)
        idtuple = self.local_canv.coords(itemId)
        if idtuple:
            x = idtuple[0]
            y = idtuple[1]
            frm = Frame(self.local_canv)
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
            self.local_canv.update_idletasks()
            canv["scrollregion"] = canv.bbox("all")
            # self.currentlyRenderedWindow = windowFrame.winfo_id()
            # self.local_canv.coords(self.currentlyRenderedWindow,idtuple)
            # Move window to the correct Location
            
            def destroyAll():
                self.remove(canvWindow)
                canv.destroy()
                aframe.destroy()
                vscroll.destroy()
                # hscroll.destroy()
                frm.destroy()
                
            self.currentlyRenderedWindow = destroyAll 
            Button(frm, text="Close", command=lambda :  destroyAll()).grid(row=2, column=0)
            
            # yScroll = Scrollbar(windowFrame, orient="vertical", command=windowFrame.yview)
            # yScroll.grid(row=0, column=1)
            # windowFrame.grid(row=0, column=0)
            # Label(aframe, text=content, background="#CCFFCC", borderwidth=6, relief="ridge", justify="left").grid(row=0,column=0)
            
