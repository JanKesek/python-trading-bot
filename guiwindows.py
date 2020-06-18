
import tkinter as tk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg,NavigationToolbar2Tk)
from matplotlib.figure import Figure, FigureCanvasBase
import mplfinance as mpf
import numpy as np
import os
import jsonpreprocess as jp
from guifetching import *


LARGE_FONT= ("Verdana", 12)


class SeaofBTCapp(tk.Tk):

    def __init__(self, *args, **kwargs):
        
        tk.Tk.__init__(self, *args, **kwargs)
        container = tk.Frame(self)
        self.plot={}
        container.pack(side="top", fill="both", expand = True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for F in (StartPage, PageOne, PageTwo):

            frame = F(container, self)

            self.frames[F] = frame

            frame.grid(row=0, column=0, sticky="nsew")
        tk.Label(self, text="ADD NEW PAIR").pack()
        self.pair_entry = tk.Entry(self)
        self.test_list = jp.fetch_tickers()
        self.pair_entry.pack()
        self.pair_entry.bind('<KeyRelease>', self.on_keyrelease)

        self.listbox = tk.Listbox(self)
        self.listbox.pack()
        self.listbox.bind('<<ListboxSelect>>', self.on_select)
        self.listbox_update(self.test_list)

        self.show_frame(StartPage)
    def evaluate(self,event):
        guiDownloadNewPair(self.pair_entry.get())
        #self.res.configure(text="DOWNLOADING PAIR: "+self.pair_entry.get())
    def show_frame(self, cont,text=None ):
        if text!=None: self.text=text
        frame = self.frames[cont]
        frame.tkraise()
        #if self.text!=None: 
        #    return self.text
    def on_keyrelease(self,event):
        value = event.widget.get()
        value = value.strip().lower()
        if value == '':
            data = self.test_list
        else:
            data = []
            for item in self.test_list:
                if value in item.lower():
                    data.append(item)                
        self.listbox_update(data)
    def listbox_update(self,data):
        self.listbox.delete(0, 'end')
        data = sorted(data, key=str.lower)
        for item in data:
            self.listbox.insert('end', item)
    def on_select(self,event):
        print(type(event.widget.get('active')))
        guiDownloadNewPair(event.widget.get('active'))
        #print('(event) previous:', event.widget.get('active'))
        #print('(event)  current:', event.widget.get(event.widget.curselection()))
        #print('---')
    def get_page(self, page_class):
        return self.frames[page_class]
        
class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)
        label = tk.Label(self, text="Show plots", font=LARGE_FONT)
        label.pack(pady=10,padx=10)
        lstOfMarkets=[x[0] for x in os.walk("data/df/")]
        lstOfMarkets=[x.split('/')[-1] for x in lstOfMarkets if x.split('/')[-1]!='']
        for f in lstOfMarkets:
            controller.plot="data/df/"+f+"/"+f+"_1h.json"
            #self.button = tk.Button(self, text=f.split(".")[0],
            #                command=lambda: controller.show_frame(PageOne))
            self.button = tk.Button(self, text=f.split(".")[0],
                            command=lambda: controller.show_frame(PageOne))
            #self.button.config(plot=controller.plot)                
            self.button.pack()

        #button2 = tk.Button(self, text="Visit Page 2",
        #                    command=lambda: controller.show_frame(PageTwo))
        #button2.pack()

class PageOne(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Page One!!!", font=LARGE_FONT)
        label.pack(pady=10,padx=10)
        self.image_label = tk.Label()
        self.image_reference = None
        self.image_label.pack()
        self.controller=controller
        self.x=self.controller.get_page(StartPage)
        button1 = tk.Button(self, text="Back to Home",
                            command=lambda: controller.show_frame(StartPage))
        button1.pack()

        button2 = tk.Button(self, text="Page Two",
                            command=lambda: controller.show_frame(PageTwo))
        button2.pack()
        button2 = tk.Button(self, text="Refresh",
                            command=lambda: self.on_show_frame(None))
        button2.pack()

        print(dir(self.master))
        self.on_show_frame(None)
        self.bind("<<ShowFrame>>",self.on_show_frame)
    def on_show_frame(self,event):
        print(self.x.button.config('text'))
        #plot=controller.show_frame(PageOne)
        #self.x.raise_frame(self)
        plot=self.x.button.config('text')[-1]
        print(plot)
        plot="data/df/"+plot+"/"+plot+"_1h.json"
        ts=getDataFrameForTk(plot)
        fig,ax=mpf.plot(ts, type='candle',style='mike',volume=True, returnfig=True,closefig=False,
                        figratio=(10,4),figscale=0.5)
        canvas=FigureCanvasTkAgg(fig,self)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

        toolbar = NavigationToolbar2Tk(canvas, self)
        toolbar.update()
    #def tkraise(self):
        #print(self.x.button.text)
     #   tk.Frame.tkraise(self)


class PageTwo(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Page Two!!!", font=LARGE_FONT)
        label.pack(pady=10,padx=10)

        button1 = tk.Button(self, text="Back to Home",
                            command=lambda: controller.show_frame(StartPage))
        button1.pack()

        button2 = tk.Button(self, text="Page One",
                            command=lambda: controller.show_frame(PageOne))
        button2.pack()
        


app = SeaofBTCapp()
app.mainloop()