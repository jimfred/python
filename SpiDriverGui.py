"""
SPI driver app.
Jim Fred 2020-05-16
Similar to the SPI driver GUI.
See https://github.com/jamesbowman/spidriver
This GUI uses tkinter because it's included with Python.
Single-threaded app using tkinter.after() to update display.
"""
import collections

from spidriver import SPIDriver  # pip install spidriver.
import serial.tools.list_ports  # pip install serial
import tkinter  # for simple GUI. Python example GUIs provided with spidriver were difficult to get working on Windows.
import tkinter.ttk
import datetime  # for formatting of uptime.
import binascii  # for hexlify.
import os


class SpiDriverGui:

    """
    Setup main GUI window.
    Main windows is a grid/table of widgets.
    Data variable is attached to each tkinter widget e.g., self.ser_num.var.set('blah')
    on_refresh_gui() will typically update each field.
    """
    def __init__(self):
        self.spi_driver = None  # none yet.
        self.grid = tkinter.Tk()  # Root window is used as a grid or table.
        self.grid.configure(padx=8, pady=8)  # add padding around grid.
        self.grid.title(os.path.basename(__file__))  # Display filename in title bar.

        # region Compose GUI widgets.

        row = 0  # row counter, used to add widgets to grid.

        # region COM port combo.
        tkinter.Label(self.grid, text='Port').grid(row=row, column=0)
        comports = [port.device for port in serial.tools.list_ports.comports()]
        self.port_combo = tkinter.ttk.Combobox(self.grid, values=comports, width=10)
        self.port_combo.grid(row=row, column=1)
        self.port_prev = None
        if len(comports) > 0:
            self.port_combo.current(len(comports)-1)  # Select last entry.
        row += 1
        # endregion COM port combo.

        # region Diagnostic fields

        def create_display_parameter(str_name, row) -> tkinter.Entry:
            lbl = tkinter.Label(self.grid, text=str_name)
            lbl.grid(row=row, column=0)
            string_var = tkinter.StringVar()
            field = tkinter.Entry(self.grid, textvariable=string_var, state="readonly", width=12)
            field.grid(row=row, column=1)
            field.var = string_var  # Bind the var to the Entry.
            return field

        self.ser_num = create_display_parameter('Serial', row); row += 1
        self.voltage = create_display_parameter('Voltage', row); row += 1
        self.current = create_display_parameter('Current', row); row += 1
        self.deg_c = create_display_parameter('Temp', row); row += 1
        self.uptime = create_display_parameter('Uptime', row); row += 1
        self.miso = create_display_parameter('MISO', row); row += 1
        self.mosi = create_display_parameter('MOSI', row); row += 1
        # endregion Diagnostic fields

        # region 3 checkboxes
        # Add three checkboxes to the same row in the table.
        # nCS is inverted (active low)
        chk_frame = tkinter.Frame(self.grid)
        v = tkinter.IntVar(); self.chk_ncs = tkinter.Checkbutton(chk_frame, text="nCS", variable=v, command=self.on_chk_ncs ); self.chk_ncs.pack(side=tkinter.LEFT); self.chk_ncs.var = v
        v = tkinter.IntVar(); self.chk_a = tkinter.Checkbutton(chk_frame, text="A", variable=v, command=self.on_chk_a ); self.chk_a.pack(side=tkinter.LEFT); self.chk_a.var = v
        v = tkinter.IntVar(); self.chk_b = tkinter.Checkbutton(chk_frame, text="B", variable=v, command=self.on_chk_b ); self.chk_b.pack(side=tkinter.LEFT); self.chk_b.var = v
        chk_frame.grid(row=row, column=0, columnspan=2);
        row += 1
        # endregion 3 checkboxes

        tkinter.Label(self.grid, text='Send bytes').grid(row=row, column=0)
        v = tkinter.StringVar()
        self.send_bytes = tkinter.Entry(self.grid, textvariable=v, width=12)
        self.send_bytes.grid(row=row, column=1)
        self.send_bytes.var = v
        v.set('12 AB')
        row += 1

        self.btn_send = tkinter.Button(self.grid, text='Transfer', command = self.on_transfer); self.btn_send.grid(row=row, column=1)

        #endregion Compose GUI widgets.

        self.grid.after(500, self.on_refresh_gui)  # Establish a refresh routine.
        self.grid.mainloop()  # launch GUI.

    #region Event handlers (typically start with 'on_').

    def on_chk_a(self):
        self.spi_driver.seta(self.chk_a.var.get())

    def on_chk_b(self):
        self.spi_driver.setb(self.chk_b.var.get())

    def on_chk_ncs(self):
        self.spi_driver.sel() if self.chk_ncs.var.get() else self.spi_driver.unsel()

    '''
    Main refresh function used to update GUI widgets.
    Called periodically using 'tkinter.after()'
    '''
    def on_refresh_gui(self):
        self.grid.after(500, self.on_refresh_gui)

        if self.port_prev != self.port_combo.get():
            self.spi_driver = None

            self.port_prev = self.port_combo.get()

            if len(self.port_prev) > 0:
                try:
                    self.spi_driver = SPIDriver(self.port_prev)
                except serial.serialutil.SerialException:
                    pass


        if self.spi_driver is not None:
            self.spi_driver.getstatus()
            self.ser_num.var.set(self.spi_driver.serial)
            self.voltage.var.set("{0:.1f} V".format(self.spi_driver.voltage))
            self.current.var.set("{0:.1f} mA".format(self.spi_driver.current))
            self.deg_c.var.set("{0:.1f} °C".format(self.spi_driver.temp))
            self.uptime.var.set(str(datetime.timedelta(seconds=self.spi_driver.uptime)))  # https://stackoverflow.com/a/775095/101252
            self.chk_ncs.var.set(not self.spi_driver.cs)
            self.chk_a.var.set(self.spi_driver.a)
            self.chk_b.var.set(self.spi_driver.b)
            return
        else:
            self.ser_num.var.set('')
            self.voltage.var.set('')
            self.current.var.set('')
            self.deg_c.var.set('')
            self.uptime.var.set('')
            self.chk_ncs.var.set(2)
            self.chk_a.var.set(2)
            self.chk_b.var.set(2)
            self.miso.var.set('')
            self.mosi.var.set('')

    """
    Exchange MOSI & MISO data with SPI Driver hardware using writeread().
    """
    def on_transfer(self):
        # bytearray.fromhex will accept spaces between bytes.
        # hexlify will create a string with a hexadecimal representation of the byte array.

        tx = bytearray.fromhex(self.send_bytes.var.get())
        self.mosi.var.set(binascii.hexlify(tx))

        rx = self.spi_driver.writeread(tx)
        self.miso.var.set(binascii.hexlify(rx))

    #endregion Event handlers



if __name__ == '__main__':
    app = SpiDriverGui()
