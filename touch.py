'''
Example to emulate bash 'touch'.
https://stackoverflow.com/a/49974693
'''

from pathlib import Path

filename = "my_file.txt"

path = Path(filename)
path.touch(exist_ok=True)  # will create file, if it exists will do nothing
file = open(path)