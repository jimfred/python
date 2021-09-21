from distutils.core import setup
from distutils.extension import Extension
from Cython.Build import cythonize

extensions = [
    Extension("wrapper", ["wrapper.pyx"], libraries=["user32"])
]
setup(
    name="wrapper",
    ext_modules=cythonize(extensions, compiler_directives={'language_level' : "3"}), requires=['Cython'] 
)