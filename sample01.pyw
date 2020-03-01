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
        label_head.configure(padx=10, pady=5)
        label_head.pack(side='top')
        
        self.frame1 = tkinter.Frame(bg='', width=100, height=50)
        self.frame1.pack(side='top', fill='both')
        
        self.label1 = tkinter.Label(self.frame1, text='Введите имя ')
        self.label1.pack(side='left')
        self.label1.configure(padx=10, pady=3)
        #self.label1.bind('<Button>', self.log_add_event)
        
        self.edit_name = tkinter.Entry(self.frame1)
        self.edit_name.pack(side='top', fill='both', expand=1)
        self.edit_name.bind("<Return>", self.log_add_event)
        self.edit_name.focus()
        
        # Текстовое окно с полосами прокруток
        self.frame_memo1 = tkinter.Frame()
        self.frame_memo1.pack(fill='both', expand=1)
        
        self.memo1 = tkinter.Text(self.frame_memo1, bg='#EEE', width=20, height=5, padx=5, pady=5)
        self.memo1['wrap'] = tkinter.NONE
        self.memo1.pack(side = 'left', fill = 'both', expand = 1)
        
        self.frame_scrollx = tkinter.Frame()
        self.frame_scrollx.pack(side='top', fill = 'x')
        
        yscroll = tkinter.Scrollbar(self.frame_memo1, orient=tkinter.VERTICAL, command=self.memo1.yview)
        xscroll = tkinter.Scrollbar(self.frame_scrollx, orient=tkinter.HORIZONTAL, command=self.memo1.xview)
        
        yscroll.pack(side='right', fill=tkinter.Y)
        xscroll.pack(side='left', expand=1, fill=tkinter.X)
        
        self.memo_wordwrap = tkinter.BooleanVar()
        self.wordwrap_cb = tkinter.Checkbutton(self.frame_scrollx, variable=self.memo_wordwrap, command=self.wordwrap_click)
        self.wordwrap_cb.pack()


        
        self.label_footer = tkinter.Label(text='', bg='#DDD')
        self.label_footer.pack(side='bottom', fill='x')

                
        # Пример
        # def open_file():
            # file_1 = open(file_name.get())
            # file_content.insert(1.0, file_1.read())
        # def save_file():
            # file_2 = open(file_name.get(), 'w')
            # file_2.write(file_content.get(1.0, END))
        # frame = Frame()
        # frame_file_content = Frame()
        # file_name = Entry(frame, bd=4, relief=GROOVE, width='25')
        # button_open = Button(frame, text=' Open the old file ', command=open_file)
        # button_save = Button(frame, text=' Save to new one ', command=save_file)
        # file_content = Text(frame_file_content, bg='#FFFFE0', width='50', height='20', wrap=NONE)
        # Yscroll = Scrollbar(frame_file_content, command=file_content.yview)
        # Xscroll = Scrollbar(orient=HORIZONTAL, command=file_content.xview)
        # file_content.configure(yscrollcommand=Yscroll.set, xscrollcommand=Xscroll.set)
        # frame.pack()
        # file_name.pack(side=LEFT)
        # button_open.pack(side=LEFT)
        # button_save.pack(side=LEFT)
        # frame_file_content.pack(fill=BOTH, expand=1)
        # file_content.pack(side=LEFT, fill=BOTH, expand=1)
        # Yscroll.pack(side=LEFT, fill=Y)
        # Xscroll.pack(side=BOTTOM, fill=X)

    def wordwrap_click(self):
        #self.memo1.insert(1.0, 'click {}\n'.format(self.memo_wordwrap.get()))
        self.memo1['wrap'] = 'word' if self.memo_wordwrap.get() else 'none'
        
    def log_add_event(self, event):
        print(event)
        #self.memo1.delete(1.0, tkinter.END)
        msg = '{:%H:%M:%S.%f} {}\n'.format(datetime.datetime.now(), self.edit_name.get())
        #msg += str(self.memo_wordwrap.get())+'\n'
        msg += str(dir(self.memo_wordwrap))+'\n'
        self.memo1.insert(1.0, msg)


class App1(tkinter.Frame):
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
root.geometry("640x480")
#app = App1(master=root)
app = App2(master=root)
app.mainloop()



#https://www.python-course.eu/tkinter_events_binds.php