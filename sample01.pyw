import tkinter

class Application(tkinter.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        #self.pack()
        self.create_widgets()

    def create_widgets(self):
        #self.bind("<Return>", self.master.destroy)
        self.master.bind('<Escape>', exit)
        
        self.label1 = tkinter.Label(text='Введите имя')
        self.label1.grid(row=1, column=1)
        self.label1.bind('<Button>', self.say_yahoo)
        
        self.edit_name = tkinter.Entry(width=30)
        self.edit_name.grid(row=1, column=2)
        self.edit_name.bind("<Return>", self.say_yahoo)
        self.edit_name.focus()
        
        self.edit_text = tkinter.Text(bg='#EEE')
        self.edit_text.grid(row=2,column=1, columnspan=2)
        
        #self.but_hi = tkinter.Button(self)
        #self.but_hi["text"] = "Hello World\n(click me)"
        #self.but_hi["command"] = self.say_hi
        #self.but_hi.pack(side="top")
        print(dir(tkinter))
        #self.memo1 = tkinter.Memo()
        self.quit = tkinter.Button(text="QUIT", fg="red", command=self.master.destroy)
        #self.quit.pack(side="bottom")
        self.quit.grid(row=3, column=1, columnspan=2)
        
    def say_yahoo(self, event):
        print(event)
        ##self.edit_text.delete(1.0, tkinter.END)
        self.edit_text.insert(1.0, self.edit_name.get())
        print('yahoo')
        #if event.keycode==13:
        #    exit()
        
    def say_hi(self):
        print("hi there, everyone!")
        self.but_hi['text'] = 'Hello!'

    

root = tkinter.Tk()
app = Application(master=root)
app.mainloop()



#https://www.python-course.eu/tkinter_events_binds.php