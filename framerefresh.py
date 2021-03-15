import tkinter as tk

class SampleApp(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        # alternate ways to create the frames & append to frames dict: comment out one or the other

        for F in (StartPage, PLG):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        # self.frames["StartPage"] = StartPage(parent=container, controller=self) 
        # self.frames["PLG"] = PLG(parent=container, controller=self)
        # self.frames["StartPage"].grid(row=0, column=0, sticky="nsew")
        # self.frames["PLG"].grid(row=0, column=0, sticky="nsew")

        self.show_frame("StartPage")

    # alternate version of show_frame: comment out one or the other

    def show_frame(self, page_name):
        for frame in self.frames.values():
            frame.grid_remove()
        frame = self.frames[page_name]
        frame.grid()

    # def show_frame(self, page_name):
        # frame = self.frames[page_name]
        # frame.tkraise()

class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        label = tk.Label(self, text="start page")
        label.pack(side="top", fill="x", pady=10)

        button1 = tk.Button(self, text="Go to Page One", command=lambda: controller.show_frame("PLG"))
        button1.pack()        

        button2 = tk.Button(self, text="focus traversal demo only")
        button2.pack()
        button2.focus_set()

        button3 = tk.Button(self, text="another dummy button")
        button3.pack()

        lbl = tk.Label(self, text="tkraise messes up focus traversal\nwhich you can see by testing the two versions of show_frame.()\nUsing grid_remove instead of tkraise solves that,\nwhile preventing frames from being unable to resize to fit their own contents.")
        lbl.pack()

class PLG(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Enter something below; the two buttons clear what you type.")
        label.pack(side="top", fill="x", pady=10)
        self.wentry = tk.Entry(self)
        self.wentry.pack(pady = 10)
        self.text = tk.Text(self)
        self.text.pack(pady = 10)
        restart_button = tk.Button(self, text="Restart", command=self.restart)
        restart_button.pack()
        refresh_button = tk.Button(self, text="Refresh", command=self.refresh) 
        refresh_button.pack()  

    def restart(self):
        self.refresh()
        self.controller.show_frame("StartPage")

    def refresh(self):
        self.wentry.delete(0, "end")
        self.text.delete("1.0", "end")
        # set focus to any widget except a Text widget so focus doesn't get stuck in a Text widget when page hides
        self.wentry.focus_set()

if __name__ == "__main__":
    app = SampleApp()
    app.mainloop()