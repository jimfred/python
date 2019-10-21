'''
Simple tkinter grid application
'''

import os
import tkinter
import tkinter.ttk
import lib.dbg


class App:

    # Add what I think is a missing integer property to tkinter.IntVar
    class IntVar2(tkinter.IntVar):
        def __init__(self):
            tkinter.IntVar.__init__(self)
            self._i = 0  # internal value for property 'i'.

        @property
        def i(self):
            return self._i

        @i.setter
        def i(self, i):
            self._i = i
            self.set(i)

    def __init__(self):
        self.root = tkinter.Tk()
        self.root.title(os.path.basename(__file__))

        tkinter.Label(self.root, text='Cnt').grid(row=1, column=0)
        self.cnt = [App.IntVar2() for i in range(5) ]
        for i in range(5):
            tkinter.Label(self.root, text='Cnt{0}'.format(i)).grid(row=0, column=1 + i)
            tkinter.Label(self.root, textvariable=self.cnt[i]).grid(row=1, column=1 + i)

        self.sum = App.IntVar2()
        tkinter.Label(self.root, text='sum').grid(row=2, column=0)
        tkinter.Label(self.root, textvariable=self.sum).grid(row=2, column=1, columnspan=5, sticky='ew')

        self.update_clock()
        self.root.mainloop()

    def update_clock(self):
        self.root.after(500, self.update_clock)
        for i in range(5):
            self.cnt[i].i += 1

        self.sum.i = sum([self.cnt[i].i for i in range(5)])

app = App()
