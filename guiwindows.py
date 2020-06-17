
import tkinter as tk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg,NavigationToolbar2Tk)
from matplotlib.figure import Figure, FigureCanvasBase
import mplfinance as mpf
import numpy as np
import os
import jsonpreprocess as jp
from PIL import Image, ImageTk
import io

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
        jp.guiDownloadNewPair(self.pair_entry.get())
        #self.res.configure(text="DOWNLOADING PAIR: "+self.pair_entry.get())
    def show_frame(self, cont ):
        frame = self.frames[cont]
        frame.tkraise()
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
        jp.guiDownloadNewPair(event.widget.get('active'))
        #print('(event) previous:', event.widget.get('active'))
        #print('(event)  current:', event.widget.get(event.widget.curselection()))
        #print('---')

        
class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)
        label = tk.Label(self, text="Show plots", font=LARGE_FONT)
        label.pack(pady=10,padx=10)

        for f in os.listdir("data/df/"):
            controller.plot="data/df/"+f
            button = tk.Button(self, text=f.split(".")[0],
                            command=lambda: controller.show_frame(PageOne))
            button.pack()

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

        button1 = tk.Button(self, text="Back to Home",
                            command=lambda: controller.show_frame(StartPage))
        button1.pack()

        button2 = tk.Button(self, text="Page Two",
                            command=lambda: controller.show_frame(PageTwo))
        button2.pack()
        ts=jp.getDataFrameForTk(controller.plot)
        fig,ax=mpf.plot(ts, type='candle',style='mike',volume=True, returnfig=True,closefig=False,
                        figratio=(10,4),figscale=0.5)
        canvas=FigureCanvasTkAgg(fig,self)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

        toolbar = NavigationToolbar2Tk(canvas, self)
        toolbar.update()




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