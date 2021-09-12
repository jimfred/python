// Dll2.cpp : Defines the exported functions for the DLL.
//

#include "pch.h"
#include "framework.h"
#include "Dll2.h"


// This is an example of an exported variable
DLL2_API int nDll2=0;

// This is an example of an exported function.
DLL2_API int fnDll2(void)
{
    nDll2 += 1;
    return nDll2;
}

