"""



"""

import serial  # pip3 install pyserial
import serial.tools.list_ports
import binascii

if __name__ == '__main__':
    #print(serial.tools.list_ports.comports())
    #print([port.device for port in serial.tools.list_ports.comports()])

    ser = serial.Serial(port='COM60', baudrate=19200, parity=serial.PARITY_EVEN, timeout=2)  # open serial port
    print('{0} is open'.format(ser.name))  # check which port was really used
    while True:
        x = ser.read(size=24)
        print('{0} bytes, {1}'.format(len(x), binascii.hexlify(bytearray(x)).decode('ascii')))
    ser.close()  # close port
    print('Done.')