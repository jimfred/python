#include "pch.h"
#include "WinCppDll.h"
#include "stdlib.h"

int __declspec(dllexport) add(int a, int b)
{
	return a + b;
}


void __declspec(dllexport) add_ref(int a, int b, int & c)
{
	c = a + b;
}


void __declspec(dllexport) set_integer_ref(int& x)
{
	x = 100;
}


void __declspec(dllexport) set_integer_ptr(int* x)
{
	*x = 200;
}


void __declspec(dllexport) set_integer_ref_ptr(int*& x)
{
	x = new int[1];
	*x = 300;
}


void __declspec(dllexport) set_integer_ptr_ptr(int** x)
{
	*x = new int[1];
	*x[0] = 400;
}

void __declspec(dllexport) set_integer_arr_ptr(int* a)
{
	a[0] = 1;
	a[1] = 3;
	a[2] = 5;
	a[3] = 7;
}

void __declspec(dllexport) set_integer_arr_ref_ptr(int*& a, int& size)
{
	size = 100000000;
	a = new int[size];
	a[0] = 2;
	a[1] = 4;
	a[2] = 6;
	a[size - 1] = 100;
}

TestStruct data[3] =
{
	{1, 1.1f, "one"},
	{2, 2.2f, "two"},
	{3, 3.3f, "three"},
};

void __declspec(dllexport) get_data(TestStruct ** p_data_array, int * p_countof)
{
	*p_data_array = &data[0];
	*p_countof = _countof(data);
}