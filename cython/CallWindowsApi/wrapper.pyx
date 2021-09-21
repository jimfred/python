# from libc.stddef cimport wchar_t

# From https://cython.readthedocs.io/en/latest/src/tutorial/strings.html
cdef extern from "Windows.h":
	ctypedef Py_UNICODE WCHAR # results in "wrapper.c(1191): warning C4996: 'PyUnicode_AsUnicode': deprecated in 3.3"
	ctypedef const WCHAR* LPCWSTR
	ctypedef void* HWND

	int __stdcall MessageBoxW(HWND hWnd, LPCWSTR lpText, LPCWSTR lpCaption, int uType)

def MessageBox(text, caption, type=0):
	MessageBoxW(NULL, text, caption, type)
	
	