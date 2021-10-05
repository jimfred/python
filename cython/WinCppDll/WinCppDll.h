#pragma once

#include "windows.h"

int __declspec(dllexport) add(int a, int b);
void __declspec(dllexport) add_ref(int a, int b, int& c);

// https://medium.com/@yusuken/calling-c-functions-from-cython-references-pointers-and-arrays-e1ccb461b6d8
void __declspec(dllexport) set_integer_ref(int& x);
void __declspec(dllexport) set_integer_ptr(int* x);
void __declspec(dllexport) set_integer_ref_ptr(int*& x);
void __declspec(dllexport) set_integer_ptr_ptr(int** x);
void __declspec(dllexport) set_integer_arr_ptr(int* a);
void __declspec(dllexport) set_integer_arr_ref_ptr(int*& a, int& size);


typedef struct TestStruct
{
	int i;
	float f;
	char const * str;
} TestStruct;

void __declspec(dllexport) get_data(TestStruct** p_data_array, int* p_countof);
