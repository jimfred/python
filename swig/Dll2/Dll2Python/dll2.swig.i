%include <windows.i> 

%module Dll2
%{
#define SWIG_FILE_WITH_INIT
#include "../Dll2/Dll2.h"
%}
#define SWIG_FILE_WITH_INIT
%include "../Dll2/Dll2.h"

   