import numpy as np
cimport numpy as np  # for np.ndarray

cdef extern from "WinCppDll.h": 
    int add(int a, int b)
    void add_ref(int a, int b, int & c)

    void set_integer_ref(int&)
    void set_integer_ptr(int*)
    void set_integer_ref_ptr(int*&)
    void set_integer_ptr_ptr(int**)
    void set_integer_arr_ptr(int*)
    void set_integer_arr_ref_ptr(int*&, int&)


def add2(int a, int b):
    return add(a, b)

def add_ref2(int a, int b, int & c):
    add_ref(a, b, c)

# https://github.com/yuyu2172/simple_cython_behaviour/blob/master/function_call/function_call.pyx

# Numpy must be initialized. When using numpy from C or Cython you must
# _always_ do that, or you will have segfaults
np.import_array()

cdef extern from "numpy/arrayobject.h":
    void PyArray_ENABLEFLAGS(np.ndarray arr, int flags)

cpdef set_integer_ref_gets_100():
    cdef int x = 0
    set_integer_ref(x)
    return x

cpdef set_integer_ptr_gets_200():
    cdef int[1] x
    set_integer_ptr(x)
    return x[0]

cpdef set_integer_ref_ptr_gets_300():
    cdef int* x
    set_integer_ref_ptr(x)
    return x[0]


cpdef pass_by_ptr_ptr_gets_400():
    cdef int* x
    set_integer_ptr_ptr(&x)
    return x[0]

cpdef pass_by_ptr_arr_gets_1357():
    # cdef np.ndarray[int, ndim=1, mode='c'] a
    # a = np.zeros((4,), dtype=np.int32)

    cdef int[4] a = [0,0,0,0]
    set_integer_arr_ptr(&a[0])
    return a

cpdef pass_by_ref_ptr_arr():
    cdef:
        int* a_ptr
        int size
        np.npy_intp shape[1]

    set_integer_arr_ref_ptr(a_ptr, size)

    # 1. Make sure that you have called np.import_array()
    # http://gael-varoquaux.info/programming/
    # cython-example-of-exposing-c-computed-arrays-in-python-without-data-copies.html
    # 2. OWNDATA flag is important. It tells the NumPy to free data when the python object is deleted.
    # https://stackoverflow.com/questions/23872946/force-numpy-ndarray-to-take-ownership-of-its-memory-in-cython/
    # You can verify that the memory gets freed when Python object is deleted by using tools such as pmap.
    shape[0] = <np.npy_intp>size
    cdef np.ndarray[int, ndim=1] a = np.PyArray_SimpleNewFromData(1, shape, np.NPY_INT32, a_ptr)
    PyArray_ENABLEFLAGS(a, np.NPY_OWNDATA)
    return a


'''
cpdef pass_by_ptr_1():
    cdef np.ndarray[int, ndim=1, mode='c'] x

    x = np.zeros((1,), dtype=np.int32)
    set_integer_ptr(&x[0])
    return x[0]


cpdef struct TestStruct:
    int i
    float f
    char * str

cpdef void get_data(TestStruct ** p_data_array, int * p_countof)


 def get_data2(r_data, countof):
	get_data(r_data, countof)
'''