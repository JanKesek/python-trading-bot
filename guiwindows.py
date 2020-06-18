
import tkinter as tk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg,NavigationToolbar2Tk)
from matplotlib.figure import Figure, FigureCanvasBase
import mplfinance as mpf
import numpy as np
import os
import jsonpreprocess as jp
from guifetching import *
from rulebased.simpleindicators import wbb_pandas

LARGE_FONT= ("Verdana", 12)


class Main(tk.Tk):

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
        frame.event_generate("<<ShowFrame>>")
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
            plot="data/df/"+f+"/"+f+"_1h.json"
            #self.button = tk.Button(self, text=f.split(".")[0],
            #                command=lambda: controller.show_frame(PageOne))
            self.button = tk.Button(self, text=f.split(".")[0],
                            command=lambda plot=plot: controller.show_frame(PageOne,plot))
            self.button.bind("<Key>", self.handle_keypress)
            #self.button.config(plot=controller.plot)                
            self.button.pack()

        #button2 = tk.Button(self, text="Visit Page 2",
        #                    command=lambda: controller.show_frame(PageTwo))
        #button2.pack()
    def handle_keypress(self,event):
        print(dir(event))
class PageOne(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Page One!!!", font=LARGE_FONT)
        label.pack(pady=10,padx=10)
        self.page_counter=0
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

        print(dir(self.master))
        self.bind("<<ShowFrame>>",lambda x: self.on_show_frame(None))
        unit_data={'1h':'Hourly','1d':'Daily','1M':'Monthly'}
        for unit in list(unit_data.keys()):           
            button3=tk.Button(self,text=unit_data[unit]+" data", command= lambda x=unit:self.on_show_frame(None, unit=x))
            button3.pack()
    def delete_and_new(self,event):
        self.toolbar.destroy()
        self.on_show_frame(None)
    def on_show_frame(self,event, unit=None):
        plot=self.controller.text
        if unit!=None:
            plot=plot.split('_')[0]+"_"+unit+".json"
        ts=getDataFrameForTk(plot)
        if self.page_counter>0: 
            self.canvas.get_tk_widget().pack_forget()
            self.toolbar.destroy()
        else:
            self.button_bb = tk.Button(self, text="Bollinger Bands",
                command=lambda x=ts: self.add_bb_indicator(None,plot=x))
            self.button_bb.pack()
        self.page_counter+=1
        self.fig,self.ax=mpf.plot(ts, type='candle',style='mike',volume=True, returnfig=True,
            closefig=False,figratio=(10,4),figscale=0.5)


        self.update_canvas()
        #self.button_bb.pack_forget()
    def add_bb_indicator(self,event, plot=None):
        self.canvas.get_tk_widget().pack_forget()
        self.toolbar.destroy()
        ts=plot
        #ts=getDataFrameForTk(plot)
        avg,lower,upper=wbb_pandas(ts,20,2)
        add0=[mpf.make_addplot(upper['Close'],color='g'),mpf.make_addplot(lower['Close'],color='b')]
        self.fig,self.ax=mpf.plot(ts, type='candle',style='mike',volume=True, returnfig=True,
            closefig=False,figratio=(10,4),figscale=0.5,addplot=add0)
        #self.button_bb.pack_forget()
        self.update_canvas()

    def update_canvas(self):
        self.canvas=FigureCanvasTkAgg(self.fig,self)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

        self.toolbar = NavigationToolbar2Tk(self.canvas, self)
        self.toolbar.update()

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
        


app = Main()
app.mainloop()