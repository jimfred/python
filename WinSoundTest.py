import os
import tkinter as tk
import winsound
import PeriodicTkAfter



if __name__ == '__main__':
    class App:

        def __init__(self):
            self.periodic_time = PeriodicTkAfter.PeriodicTkAfter(1000)  # Timer.
            self.cnt = 0

            self.root = tk.Tk()
            self.root.title(os.path.basename(__file__))

            winsound.SND_ASYNC = True

            tk.Button(self.root, text="500", command=lambda: winsound.Beep(500, 1000), width=10, height=1).grid(row=0, column=0, sticky='w')
            tk.Button(self.root, text="1000", command=lambda: winsound.Beep(1000, 1000), width=10).grid(row=1, column=0, sticky='w')
            tk.Button(self.root, text="2000", command=lambda: winsound.Beep(frequency=2000, duration=2000), width=10).grid(row=2, column=0,
                                                                                                        sticky='w')

            self.update()
            self.root.mainloop()

        def update(self):
            self.root.after(self.periodic_time.get_next_delta_ms(), self.update)
            print(self.cnt)
            self.cnt += 1

    app = App()
