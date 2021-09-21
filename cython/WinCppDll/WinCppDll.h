#pragma once

#include "windows.h"

int __declspec(dllexport) add(int a, int b);

typedef struct TestStruct
{
	int i;
	float f;
	char const * str;
} TestStruct;