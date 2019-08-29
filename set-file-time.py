'''
Example to change a file's time.
'''

import os
import datetime

def set_mod_time(file_str: str, iso_date_time_str: str):
    # date = datetime.datetime.now()
    date = datetime.datetime.strptime(iso_date_time_str, "%Y-%m-%d %H:%M:%S")

    timestamp = date.timestamp() # seconds passed since epoch in local time.

    os.utime(file_str, (timestamp, timestamp)) # accesstime, modifiedtime
    #os.utime(file_str, None) # None is now.

set_mod_time("my_file.txt", "2019-08-21 15:39:00")