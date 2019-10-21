"""



"""

import serial
import serial.tools.list_ports  # pip3 install pyserial
import binascii

if __name__ == '__main__':
    # print(serial.tools.list_ports.comports())
    for port in serial.tools.list_ports.comports():
        print('{0}'.format(port.device))
        print('\tdescription: {0}'.format(port.description))
        print('\thwid: {0}'.format(port.hwid))
        print('\tvid: {0}'.format(port.vid))
        print('\tpid: {0}'.format(port.pid))
        print('\tserial_number: {0}'.format(port.serial_number))
        print('\tlocation: {0}'.format(port.location))
        print('\tmanufacturer: {0}'.format(port.manufacturer))
        print('\tproduct: {0}'.format(port.product))
        print('\tinterface: {0}'.format(port.interface))

    ser1 = serial.Serial(port='COM104', baudrate=19200, parity=serial.PARITY_NONE, timeout=2)  # open serial port
    print('{0} is open'.format(ser1.name))  # check which port was really used
    ser2 = serial.Serial(port='COM105', baudrate=19200, parity=serial.PARITY_NONE, timeout=2)  # open serial port
    print('{0} is open'.format(ser2.name))  # check which port was really used

    while True:

        ser1.write('abcdef'.encode())
        barr2 = ser2.read(size=6)
        print('Ser2 read {0} bytes, {1}'.format(len(barr2), bytearray(barr2).decode('ascii')))

        ser2.write('ABCDEF'.encode())
        barr1 = ser1.read(size=6)
        print('Ser1 read {0} bytes, {1}'.format(len(barr1), bytearray(barr1).decode('ascii')))

    ser.close()  # close port

    print('Done.')