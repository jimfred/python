import os
import tkinter as tk
import tkinter.ttk as ttk
import pyttsx3  # pip3 install pyttsx3
import PeriodicTkAfter

class TextToSpeech:

    def __init__(self):
        self.engine = pyttsx3.init()

        self.engine = pyttsx3.init()
        voices = self.engine.getProperty('voices')

        print(voices[0])
        voices[0].gender = 'male'

        self.engine.say('Start!')
        self.engine.runAndWait()

        #print(self.engine.getProperty('rate'))
        self.engine.setProperty('rate', 300)

    def say(self, strMsg):
        self.engine.say(strMsg)
        self.engine.runAndWait()

if __name__ == '__main__':
    class App:

        def __init__(self):
            self.talker = TextToSpeech()
            self.periodic_time = PeriodicTkAfter.PeriodicTkAfter(1000)  # Timer.
            self.cnt = 0

            self.root = tk.Tk()
            self.root.title(os.path.basename(__file__))

            self.btn_pass = tk.Button(self.root, text="Say 'Pass'", command=lambda: self.talker.say('Pass!'), width=10, height=1)
            self.btn_pass.grid(row=2, column=0, sticky='w')

            self.btn_fail = tk.Button(self.root, text="Say 'Fail'", command=lambda: self.talker.say('Fail!'), width=10)
            self.btn_fail.grid(row=1, column=0, sticky='w')

            self.btn_say = tk.Button(self.root, text='Say...', command=lambda: self.talker.say(self.txt_say.get('1.0', 'end')), width=10)
            self.btn_say.grid(row=0, column=0, sticky='w')

            self.txt_say = tk.Text(self.root, width=10, height=1)
            self.txt_say.grid(row=0, column=1, sticky='w')
            self.txt_say.insert('1.0', 'Testing 1 2 3!')

            self.update()
            self.root.mainloop()

        def update(self):
            self.root.after(self.periodic_time.get_next_delta_ms(), self.update)
            #self.talker.say(str(self.cnt))
            print(self.cnt)
            self.talker.say('tik')
            self.cnt += 1

    app = App()
