from distutils.core import setup
from distutils.extension import Extension
from Cython.Build import cythonize
import numpy

extensions = [
    Extension("WinCppDll", ["WinCppDllwrapper.pyx"],
        include_dirs=[numpy.get_include()],
        libraries=["WinCppDll"],
        language="c++")
]
setup(
    name="WinCppDll",
    ext_modules=cythonize(extensions, compiler_directives={'language_level' : "3"}), requires=['Cython'] 
)