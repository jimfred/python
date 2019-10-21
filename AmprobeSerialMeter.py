"""
Driver for communications to Amprobe AM-140-A volt/multi-meter.

rx() returns float of value measured.
See PDF called 'Protocol for 500000-count multimeter series', dated 2008/12/16, 2-pages.
Checksum not implemented.
Blocking call to rx() but tx and rx can be called separately.

# pip3 install pyserial

"""

import serial


class AmprobeSerialMeter:

    # command byte array. Never changes.
    cmd_bar = b'\x10\x02\x00\x00\x00\x00\x10\x03'

    def __init__(self):
        self.port_serial = None
        self.rsp_bar = b''
        self.val = float('nan')

    def open(self, port):
        # open serial port
        self.port_serial = serial.Serial(
            port=port,
            baudrate=9600,
            parity=serial.PARITY_NONE,
            timeout=0.2,
            inter_byte_timeout=0.1)

        #print('{0} is open.'.format(self.port_serial.name))  # check which port was really used

    def close(self):
        self.port_serial.close()

    def tx(self, cmd_bar=cmd_bar):
        if self.port_serial is None or not self.port_serial.is_open:
            return
        self.port_serial.flush()
        self.port_serial.write(cmd_bar)

    def rx(self) -> float:
        if self.port_serial is None or not self.port_serial.is_open:
            self.rsp_bar = b''
        else:
            self.rsp_bar = self.port_serial.read_until(b'\x10\x03')  # response ends with '\x10\x02'
        # print(rsp_bar)
        if len(self.rsp_bar) == 14 and self.rsp_bar[0:4] == b'\x10\x02\x01\x07' and self.rsp_bar[9:11] == b'OL':  # if
            self.val = float('inf')
        elif len(self.rsp_bar) == 0:
            # This occurs when the range changes.
            # Keep old value as-is
            self.val = self.val
        elif len(self.rsp_bar) == 22 and self.rsp_bar[0:4] == b'\x10\x02\x00\x0F':
            # Expect number, in scientific notation, in bytes 8 thru 18 inclusive.
            # remove the space before the E.
            s = bytearray(self.rsp_bar[8:19]).decode('ascii').replace(' E', 'E')
            # At this point, s is expected to be a number of the form -0.0006E-1.
            # Convert to float.
            try:
                self.val = float(s)
            except ValueError:
                self.val = 0
        else:
            self.val = float('nan')

        return self.val

    # From table 1 in 'Protocol for 500000-count multimeter series'
    def get_range(self) -> str:

        if len(self.rsp_bar) == 0:
            return '?'
        elif self.rsp_bar[5] == 0b00000000 and self.rsp_bar[4] == 0b00000101:
            return 'AcV'
        elif self.rsp_bar[5] == 0b00000000 and self.rsp_bar[4] == 0b00000110:
            return 'DcV'
        elif self.rsp_bar[5] == 0b00000000 and self.rsp_bar[4] == 0b00000111:
            return 'AC+DCV'
        elif self.rsp_bar[5] == 0b00000000 and self.rsp_bar[4] == 0b00001000:
            return 'Cx'
        elif self.rsp_bar[5] == 0b00000000 and self.rsp_bar[4] == 0b00010100:
            return 'Dx'
        elif self.rsp_bar[5] == 0b00000000 and self.rsp_bar[4] == 0b00100000:
            return '°C'
        elif self.rsp_bar[5] == 0b00000000 and self.rsp_bar[4] == 0b01000000:
            return '°F'
        elif self.rsp_bar[5] == 0b00000000 and self.rsp_bar[4] == 0b10000000:
            return 'Ohm'
        elif self.rsp_bar[5] == 0b00000001 and self.rsp_bar[4] == 0b10000000:
            return 'Conti' # Beep mode.
        elif self.rsp_bar[5] == 0b00000010 and self.rsp_bar[4] == 0b00000001:
            return 'AcA'
        elif self.rsp_bar[5] == 0b00000010 and self.rsp_bar[4] == 0b00000010:
            return 'DcA'
        elif self.rsp_bar[5] == 0b00000010 and self.rsp_bar[4] == 0b00000011:
            return 'Ac+DcA'
        elif self.rsp_bar[5] == 0b00000100 and self.rsp_bar[4] == 0b00000000:
            return 'Hz'
        elif self.rsp_bar[5] == 0b00001000 and self.rsp_bar[4] == 0b00000000:
            return 'Duty%'
        elif self.rsp_bar[5] == 0b00100000 and self.rsp_bar[4] == 0b00000000:
            return 'dB'
        elif self.rsp_bar[5] == 0b00000000 and self.rsp_bar[4] == 0b00000100: # not documented but condition seen.
            return 'Diode'
        else:
            return '?'

# test case, hard coded for a COM port. Reads forever.
if __name__ == '__main__':

    import time
    import EngineeringNotation
    import os

    com_port_name = 'COM6'
    uut = AmprobeSerialMeter()
    try:
        uut.open(com_port_name)
    except serial.serialutil.SerialException as e:
        msg = None
        if os.name == 'nt':
            # When unplugged:
            #    could not open port 'COM6': FileNotFoundError(2, 'The system cannot find the file specified.', None, 2)
            if str(e).find('FileNotFoundError') > -1:
                msg = com_port_name + ' not found'
            # When already open:
            #    could not open port 'COM6': PermissionError(13, 'Access is denied.', None, 5)
            elif str(e).find('PermissionError') > -1:
                msg = com_port_name + ' might already be open'
        if msg is None:
            msg = str(e)
        print(msg)

        exit(-1)

    time.sleep(0.2)
    uut.tx()
    time.sleep(0.2)
    uut.tx()

    while True:
        f = uut.rx()
        # print float, response string and range.
        print('{0} ({1}) {2}'.format(EngineeringNotation.to_string(f, 3), uut.rsp_bar, uut.get_range()))
        uut.tx()
        time.sleep(1)

