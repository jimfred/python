/** 
 * File : example.c 
 * Based on the 'hurry' example at http://www.swig.org/tutorial.html
 * This is compiled in Visual Studio 2019, 64-bit, for Windows.
 * Environment vars:
 *   PYTHON_INCLUDE: blah\Python\Python39\include
 *   PYTHON_LIB: blah\Python\Python39\libs\python39.lib
 * The 'example' project in example_dll.vcxproj generates example.dll which is copied to /_example.pyd.
 * RunMe.py exercises _example.pyd.
 * A custom build operation was created for example.i that runs ./swig.bat which has a command like: "C:\Program Files\SWIG\swigwin-4.0.2\swig.exe" -python -o example_wrap.c example.i
 *   
*/
 
 #include <time.h>
 #include <stdio.h>

 double My_variable = 3.21;
 
 int fact(int n) {
     if (n <= 1) return 1;
     else return n*fact(n-1);
 }
 
 int my_mod(int x, int y) {
     return (x%y);
 }
 	
 char *get_time()
 {
     time_t rawtime = 0;
     time(&rawtime);
     struct tm ltime = { 0 };
     localtime_s(&ltime, &rawtime);

     static char result[52]; // it's ok to return the address of a static (not on the stack) buffer.

     sprintf_s(
         result, 
         sizeof(result),
         "%04d-%02d-%02d %02d:%02d:%02d\n",
         1900 + ltime.tm_year,
         1 + ltime.tm_mon,
         ltime.tm_mday, 
         ltime.tm_hour,
         ltime.tm_min, 
         ltime.tm_sec
     );

     return result;
 }