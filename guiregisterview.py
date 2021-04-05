import tkinter as tk
from guifetching import register_api_key

class PageRegister(tk.Frame):
    def __init__(self, parent, controller): 
        self.login=""
        self.pubkey=""
        self.privkey=""
        tk.Frame.__init__(self, parent)
        tk.Label(self,text="Login do giełdy").pack()
        amount_btn = tk.Entry(self)
        amount_btn.pack()
        amount_btn.bind('<KeyRelease>', self.on_keyrelease_login)
        tk.Label(self,text="Klucz publiczny").pack()
        pub_entry = tk.Entry(self, show="*")
        pub_entry.pack()
        pub_entry.bind('<KeyRelease>', self.on_keyrelease_pubkey)
        tk.Label(self,text="Klucz prywatny").pack()
        priv_entry = tk.Entry(self, show="*")
        priv_entry.pack()
        priv_entry.bind('<KeyRelease>', self.on_keyrelease_privkey)

        self.buy_button = tk.Button(self,text="Zarejestruj", command=lambda: register_api_key(self.login,self.pubkey,self.privkey))
        self.buy_button.place(x=self.winfo_screenwidth()/3+40,y=100)
    def on_keyrelease_login(self,event):
        self.login = event.widget.get()
        print(self.login)
    def on_keyrelease_pubkey(self,event):
        self.pubkey = event.widget.get()
        print(self.pubkey)
    def on_keyrelease_privkey(self,event):
        self.privkey = event.widget.get()
        print(self.privkey)
