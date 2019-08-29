'''
tkinter-counter.py
JimFred 2019-08-28

Simple tkinter app that implements a simple counter.
Uses tk.after as a timer. One Tk.Button clears the counter.
'''

from tkinter import *

class App:
    def __init__(self):
        self.tk = Tk()
        self.cnt = IntVar()
        self.w = Label(self.tk, textvariable=self.cnt)
        self.w.pack()
        self.btnClear = Button(self.tk, text='Clear', command = lambda: self.cnt.set(0))
        self.btnClear.pack()
        self.tk.after(1000, self.on_tick)
        self.tk.mainloop()

    def on_tick(self):
        self.tk.after(1000, self.on_tick)
        self.cnt.set( self.cnt.get() + 1 )

app = App()
