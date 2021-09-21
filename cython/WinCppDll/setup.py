from distutils.core import setup
from distutils.extension import Extension
from Cython.Build import cythonize

extensions = [
    Extension("WinCppDll", ["WinCppDll.pyx"], libraries=["WinCppDll"])
]
setup(
    name="WinCppDll",
    ext_modules=cythonize(extensions, compiler_directives={'language_level' : "3"}), requires=['Cython'] 
)