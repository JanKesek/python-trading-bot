
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

        self.show_frame(StartPage)

    def show_frame(self, cont, ):

        frame = self.frames[cont]
        frame.tkraise()

        
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
        #print(parent)
        #print(controller)
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
        #fig = Figure(figsize=(5, 4), dpi=100)
        ts=jp.getDataFrameForTk(controller.plot)
        #img_buffer = io.BytesIO()
        #fig,ax=mpf.plot(ts, type='candle', savefig=dict(fname=img_buffer, dpi=192),closefig=False)
        fig,ax=mpf.plot(ts, type='candle',style='mike',volume=True, returnfig=True,closefig=False,
                        figratio=(10,4),figscale=0.5)
        #canvas = FigureCanvasBase(fig)
        #top=tk.Toplevel()
        canvas=FigureCanvasTkAgg(fig,self)
        #chart_type.get_tk_widget().pack()
        #chartLayout.addWidget(canvas)
        #df = df[['First Column','Second Column']].groupby('First Column').sum()
        #ts.plot(legend=True, ax=ax)
        #ax.set_title('The Title for your chart')
        #plt.close('all')
        #img_buffer.seek(0)
        #pil_image = Image.open(img_buffer)
        #pil_image = pil_image.resize((self.root.winfo_width(), self.root.winfo_height() - (self.root.winfo_reqheight() - self.image_label.winfo_height())))
        #pil_image = pil_image.resize((1340, 500))
    
        #self.image_reference = ImageTk.PhotoImage(pil_image)
        #self.image_label.configure(image=self.image_reference)
        #self.image_label.image = self.image_reference
        
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