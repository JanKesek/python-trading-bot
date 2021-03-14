
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
from threading import Thread
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

        for F in (StartPage, PageOne, PageTwo, PageThree):

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

        #self.outputField = tk.Label(self, text=fetchall_api())
        #self.outputField.pack()
        self.show_frame(StartPage)
    def show_frame(self, cont,text=None ):
        if text!=None: self.text=text
        frame = self.frames[cont]
        frame.event_generate("<<ShowFrame>>")
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
        runthread=Thread(target=lambda x=event.widget.get('active') : guiDownloadNewPair(x))
        runthread.start()
    def get_page(self, page_class):
        return self.frames[page_class]
        
class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)
        label = tk.Label(self, text="Show plots", font=LARGE_FONT)
        label.pack(pady=10,padx=10)
        lstOfMarkets=[x[0] for x in os.walk("data/df/")]
        lstOfMarkets=[x.split('/')[-1] for x in lstOfMarkets if x.split('/')[-1]!='']
        self.column_n=self.winfo_screenwidth()/3+40
        #button_frame = tk.Frame(self.grid)
        #button_frame.grid(row=1,column=3,columnspan=2)
        #button_frame.pack(side="bottom", fill="x", expand=False)
        #canvas.pack(side="top", fill="both", expand=True)

        for f in lstOfMarkets:
            plot="data/df/"+f+"/"+f+"_1h.json"
            self.button = tk.Button(self, text=f.split(".")[0],
                            command=lambda plot=plot: controller.show_frame(PageOne,plot))
            self.button.bind("<Key>", self.handle_keypress)
            #self.button.grid(row=0,column=column_n)
            self.column_n+=100
            self.button.place(x=self.column_n,y=0)
            #self.button.pack()
        #button_frame.grid_columnconfigure(0,weight=1)
        #button2 = tk.Button(self, text="Visit Page 2",
        #                    command=lambda: controller.show_frame(PageTwo))
        #button2.pack()

        self.tradeButton = tk.Button(self, text="New BitBay trade",
                            command=lambda : controller.show_frame(PageThree))
        self.tradeButton.bind("<Key>", self.handle_keypress)
            #self.button.grid(row=0,column=column_n)
        self.tradeButton.place(x=self.winfo_screenwidth()/3+40,y=100)

    def handle_keypress(self,event):
        print(dir(event))
class PageOne(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        #label = tk.Label(self, text="Page One!!!", font=LARGE_FONT)
        #label.pack(pady=10,padx=10)
        self.page_counter=0
        self.image_label = tk.Label()
        self.image_reference = None
        self.image_label.pack()
        self.controller=controller
        self.x=self.controller.get_page(StartPage)
        button1 = tk.Button(self, text="Back to Home",
                            command=lambda: controller.show_frame(StartPage))
        button1.pack()

        #button2 = tk.Button(self, text="Page Two",
        #                    command=lambda: controller.show_frame(PageTwo))
        #button2.pack()

        self.bind("<<ShowFrame>>",lambda x: self.on_show_frame(None))
        unit_data={'1h':'Hourly','1d':'Daily','1M':'Monthly'}
        column_n=self.winfo_screenwidth()/5
        for unit in list(unit_data.keys()):     
            button3=tk.Button(self,text=unit_data[unit]+" data", command= lambda x=unit:self.on_show_frame(None, unit=x))
            button3.place(x=column_n,y=0)
            column_n+=100
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
            self.button_bb.place(x=self.winfo_screenwidth()*0.7,y=0)
        self.page_counter+=1
        self.fig,self.ax=mpf.plot(ts, type='candle',style='mike',volume=True, returnfig=True,
            closefig=False,figratio=(10,4),figscale=0.5)


        self.update_canvas()
        #self.button_bb.pack_forget()
    def add_bb_indicator(self,event, plot=None):
        self.canvas.get_tk_widget().pack_forget()
        self.toolbar.destroy()
        avg,lower,upper=wbb_pandas(plot,20,2)
        add0=[mpf.make_addplot(upper['Close'],color='g'),mpf.make_addplot(lower['Close'],color='b')]
        self.fig,self.ax=mpf.plot(plot, type='candle',style='mike',volume=True, returnfig=True,
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
class PageThree(tk.Frame):
    def __init__(self, parent, controller): 
        tk.Frame.__init__(self, parent)
        self.market = None
        self.amount = 1
        self.price = 50
        self.market_list = fetch_markets_bitbay()
        self.listbox = tk.Listbox(self)
        self.listbox.pack()
        self.listbox.bind('<<ListboxSelect>>', self.on_select)
        self.listbox_update(self.market_list)
        tk.Label(self,text=self.current_amount()).pack()
        amount_btn = tk.Entry(self)
        amount_btn.pack()
        amount_btn.bind('<KeyRelease>', self.on_keyrelease_amount)
        tk.Label(self,text=self.current_price()).pack()
        price_btn = tk.Entry(self)
        price_btn.pack()
        price_btn.bind('<KeyRelease>', self.on_keyrelease_price)
        self.buy_button = tk.Button(self,text="Kup", command=lambda: buy_bitbay(self.amount,self.price, self.market))
        self.buy_button.place(x=self.winfo_screenwidth()/3+40,y=100)
    def on_select(self,event):
        print(type(event.widget.get('active')))
        self.market = event.widget.get('active')
    def listbox_update(self,data):
        self.listbox.delete(0, 'end')
        data = sorted(data, key=str.lower)
        for item in data:
            self.listbox.insert('end', item)
    def current_amount(self):
        market=""
        if self.market is not None:
            market = self.market.split("_")[0]
        return "Ilość {} do kupienia".format(market)
    def current_price(self):
        market=""
        if self.market is not None:
            market = self.market.split("_")[1]
        return "Za ile {} chce kupić".format(market)
    def on_keyrelease_price(self,event):
        self.price = event.widget.get()
        print(self.price)
    def on_keyrelease_amount(self,event):
        self.amount =event.widget.get()
        print(self.amount)
app = Main()
app.mainloop()