"""
Wrapper to auto-update a var if another var changes.
Taken from https://stackoverflow.com/a/21837256/101252
"""

import tkinter
import typing  # for type hints.

update_in_progress = False  # prevent an infinitely recursive echo chamber.


def on_var_change(var, op: typing.Callable) -> None:
    """
    on_var_change
    Add an operation to perform when variable 'var' has changed.
    For example usage, see __main__.
    """
    def do_this(op2: typing.Callable) -> None:
        """
        This local function is only used here.
        It wraps the passed-in operation with exception handling and handles usage of global semaphore.
        """
        global update_in_progress
        if update_in_progress:
            return
        try:
            update_in_progress = True
            op2()
        except (ValueError, tkinter.TclError):
            pass
        finally:
            update_in_progress = False
        return

    var.trace_add("write", lambda name, index, mode, op2=op: do_this(op))


if __name__ == '__main__':
    root = tkinter.Tk()
    hex_number = tkinter.StringVar()
    dec_number = tkinter.IntVar()

    tkinter.Label(root, text="Hex").grid(row=0, column=0)
    tkinter.Label(root, text="Dec").grid(row=0, column=1)

    tkw_hex = tkinter.Entry(root, textvariable=hex_number)
    tkw_dec = tkinter.Entry(root, textvariable=dec_number)

    tkw_hex.grid(row=1, column=0)
    tkw_dec.grid(row=1, column=1)

    tkinter.Label(root, text="F").grid(row=2, column=0)
    tkinter.Label(root, text="C").grid(row=2, column=1)

    t_f_val = tkinter.DoubleVar()
    t_f_tkw = tkinter.Entry(root, textvariable=t_f_val)
    t_f_tkw.grid(row=3, column=0)

    t_c_val = tkinter.DoubleVar()
    t_c_tkw = tkinter.Entry(root, textvariable=t_c_val)
    t_c_tkw.grid(row=3, column=1)

    on_var_change(hex_number, op=lambda: (dec_number.set(int(hex_number.get(), base=16))))
    on_var_change(dec_number, op=lambda: (hex_number.set(hex(dec_number.get()))))
    on_var_change(t_f_val, op=lambda: (t_c_val.set((t_f_val.get() - 32.0)*5.0/9.0)))
    on_var_change(t_c_val, op=lambda: (t_f_val.set(t_c_val.get() * 9.0 / 5.0 + 32.0)))

    root.mainloop()
