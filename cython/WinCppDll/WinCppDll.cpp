#include "pch.h"
#include "WinCppDll.h"
#include "stdlib.h"

extern "C" int __declspec(dllexport) add(int a, int b)
{
	return a + b;
}

TestStruct data[3] =
{
	{1, 1.1f, "one"},
	{2, 2.2f, "two"},
	{3, 3.3f, "three"},
};

__declspec(dllexport) void get_data(TestStruct& r_data, int& countof)
{
	r_data = data[0];
	countof = _countof(data);
}