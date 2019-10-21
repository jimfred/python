"""
Test GUI for Amprobe AM-140-A volt/multi-meter.

"""

import os
import tkinter
import tkinter.ttk
import json
import serial  # pip3 install pyserial
import serial.tools.list_ports
import EngineeringNotation  # local file.
import AmprobeSerialMeter  # local file.


class App:

    class Config:
        @staticmethod
        def get_name():
            return os.path.basename(__file__) + '.json'

        def __init__(self):
            self.port_name = 'COM1'
            self.x = '123.456'
            try:
                f = open(self.get_name())
                x = json.load(f)
                self.port_name = x['port_name']
                self.x = x['x']
            except FileNotFoundError:
                self.save()

        def save(self):
            with open(self.get_name(), 'w') as json_file:
                json.dump(self.__dict__, json_file)

    @staticmethod
    def get_all_serial_ports() -> []:
        return [port.device for port in serial.tools.list_ports.comports()]

    def __init__(self):
        self.meter = AmprobeSerialMeter.AmprobeSerialMeter()
        self.root = tkinter.Tk()
        self.root.title(os.path.basename(__file__))

        self.config = self.Config()

        row = 0
        tkinter.Label(self.root, text='Port').grid(row=row, column=0)
        self.port_combo = tkinter.ttk.Combobox(self.root, values=self.get_all_serial_ports())
        self.port_combo.set(self.config.port_name)
        self.port_prev = None
        self.port_combo.grid(row=row, column=1)

        row += 1
        self.port_open = tkinter.StringVar(value='?')
        tkinter.Label(self.root, text='Port open?').grid(row=row, column=0)
        tkinter.Entry(self.root, textvariable=self.port_open, state="readonly").grid(row=row, column=1)

        row += 1
        self.meter_value = tkinter.DoubleVar(value='?')
        tkinter.Label(self.root, text='Meter reading').grid(row=row, column=0)
        tkinter.Entry(self.root, textvariable=self.meter_value, state="readonly").grid(row=row, column=1)

        row += 1
        self.meter_range = tkinter.StringVar(value='?')
        tkinter.Label(self.root, text='Meter range').grid(row=row, column=0)
        tkinter.Entry(self.root, textvariable=self.meter_range, state="readonly").grid(row=row, column=1)

        row += 1
        self.raw_response = tkinter.StringVar(value='?')
        tkinter.Label(self.root, text='Raw response').grid(row=row, column=0)
        tkinter.Entry(self.root, textvariable=self.raw_response, state="readonly").grid(row=row, column=1)

        row += 1
        self.update_count = tkinter.IntVar()
        tkinter.Label(self.root, text='Running').grid(row=row, column=0)
        tkinter.Entry(self.root, textvariable=self.update_count, state="readonly").grid(row=row, column=1)

        self.update_clock()
        self.root.mainloop()

    def update_clock(self):
        self.root.after(500, self.update_clock)
        try:
            self.update_count.set(self.update_count.get() + 1)
        except:
            self.update_count.set(0)

        if self.port_prev != self.port_combo.get():
            try:
                self.meter.close()
            except:
                pass

            self.port_prev = self.port_combo.get()

            try:
                self.meter.open(self.port_prev)
            except:
                pass

        if self.meter.port_serial is not None and self.meter.port_serial.is_open:
            self.port_open.set('yes')
        else:
            self.port_open.set('no')

        f = self.meter.rx()
        self.meter_value.set('(None)' if 0 == len(self.meter.rsp_bar) else EngineeringNotation.to_string(f, 3))
        self.meter_range.set('(None)' if 0 == len(self.meter.rsp_bar) else self.meter.get_range())
        self.raw_response.set('(None)' if 0 == len(self.meter.rsp_bar) else self.meter.rsp_bar.hex())

        self.meter.tx()


if __name__ == '__main__':
    #print(App.get_all_serial_ports())
    #exit(0)
    app = App()

