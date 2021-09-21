
cdef extern from "WinCppDll.h":
	int add(int a, int b)

def add2(int a, int b):
	return add(a, b)