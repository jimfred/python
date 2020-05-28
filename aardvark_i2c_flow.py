"""
Read flow from a Honeywell Zephyr using an Aardvark i2c.

------  -----  ---  --------
Sensor              Aardvark
pin                 pin
------  -----  ---  --------
 1      NC
 2      SCL    yel    1
 3      VVDD   red    4        20 mA max
 4      grnd   grn    2
 5      SDA    orn    3
 6      NC
------  -----  ---  --------

"""

from aardvark_py import *  # pip install aardvark-py

aa_find_devices(1)
aardvark = aa_open(0)

aa_features(aardvark)
aardvark_py.aa_i2c_bitrate(aardvark, 10)
aardvark_py.aa_i2c_pullup(aardvark, aardvark_py.AA_I2C_PULLUP_BOTH)

iterations = 100  # loop several times to
flow = [None] * iterations
for i in range(iterations):

    data_in = array_u08(2)  # allocate a 2-byte array to receive read-data.
    aardvark_py.aa_i2c_read(aardvark, 0x49, aardvark_py.AA_I2C_NO_FLAGS, data_in)
    raw_value = data_in[0] * 256 + data_in[1]

    calibration_factor = 1.25  # derived from bubble-o-meter.
    flow[i] = 10 * (raw_value / 16384.0 - 0.1) / 0.8 * calibration_factor

    # print("{0:X} {1:x}, {2}".format(data_in[0], data_in[1], flow[i]))

print("{:.2f} L/m".format(sum(flow) / len(flow)))

aa_close(aardvark)

