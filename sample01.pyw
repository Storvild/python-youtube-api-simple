import tkinter
import datetime

class App2(tkinter.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.create_widgets()
    
    def create_widgets(self):
        self.master.bind('<Escape>', exit)
        
        label_head  = tkinter.Label(text='Заголовок')
        label_head.pack(side='top')
        
        self.frame1 = tkinter.Frame(bg='', width=100, height=50)
        self.frame1.pack(side='top', fill='both')
        
        self.label1 = tkinter.Label(self.frame1, text='Введите имя ')
        self.label1.pack(side='left')
        #self.label1.bind('<Button>', self.log_add_event)
        
        self.edit_name = tkinter.Entry(self.frame1)
        self.edit_name.pack(side='top', fill='both', expand=1)
        self.edit_name.bind("<Return>", self.log_add_event)
        self.edit_name.focus()
        
        self.edit_text = tkinter.Text(bg='#EEE')
        self.edit_text.pack(side = 'top', fill = 'both', expand = 1)
        self.label_footer = tkinter.Label(text='', bg='#DDD')
        self.label_footer.pack(side='bottom', fill='x')
        
    def log_add_event(self, event):
        print(event)
        #self.edit_text.delete(1.0, tkinter.END)
        msg = '{:%H:%M:%S.%f} {}\n'.format(datetime.datetime.now(), self.edit_name.get())
        self.edit_text.insert(1.0, msg)


class Application(tkinter.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        #self.pack()
        self.create_widgets()


    def create_widgets(self):
        #self.bind("<Return>", self.master.destroy)
        self.master.bind('<Escape>', exit)
        
        #frame1 = tkinter.Frame(self.master)
        #frame1.grid()
        self.label1 = tkinter.Label(text='Введите имя')
        self.label1.grid(row=1, column=1)
        self.label1.bind('<Button>', self.log_add_event)
        
        self.edit_name = tkinter.Entry(width=30)
        self.edit_name.grid(row=1, column=2)
        self.edit_name.bind("<Return>", self.log_add_event)
        self.edit_name.focus()
        
        self.edit_text = tkinter.Text(bg='#EEE')
        self.edit_text.grid(row=2,column=1, columnspan=2)
        
        print(dir(tkinter))
        self.quit = tkinter.Button(text="QUIT", fg="red", command=self.master.destroy)
        self.quit.grid(row=3, column=1, columnspan=2)
        
    def log_add_event(self, event):
        print(event)
        ##self.edit_text.delete(1.0, tkinter.END)
        msg = '{:%H:%M:%S.%f} {}\n'.format(datetime.datetime.now(), self.edit_name.get())
        
        #self.edit_text.insert(1.0, msg)
        self.edit_text.insert(1.0, msg)
        print('yahoo')
        #if event.keycode==13:
        #    exit()
    

        
    def say_hi(self):
        print("hi there, everyone!")
        self.but_hi['text'] = 'Hello!'

    

root = tkinter.Tk()
#app = Application(master=root)
app = App2(master=root)
app.mainloop()



#https://www.python-course.eu/tkinter_events_binds.php