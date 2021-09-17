'''
From https://cython.readthedocs.io/en/latest/src/tutorial/external.html,
has the atoi example, and a couple of others.
Built with 'python setup.py build_ext --inplace'
'''

from libc.stdlib cimport atoi
from cpython.version cimport PY_VERSION_HEX
from libc.math cimport sin

cdef parse_charptr_to_py_int(char* s):
    assert s is not NULL, "byte string value is NULL"
    return atoi(s)  # note: atoi() has no error detection!
	

cdef double f(double x):
    return sin(x * x)

print("Hello World")
print(f'Version: {PY_VERSION_HEX}')
print(parse_charptr_to_py_int("  123  "))
print(f(1))


	
	