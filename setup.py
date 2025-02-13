#!/usr/bin/env sage-python23

from setuptools import setup, Extension
from os import path
from Cython.Build import cythonize
import Cython.Compiler.Options
from sage.env import sage_include_directories

ext_modules = [
        Extension('slabbe.kolakoski_word_pyx',
            sources = [path.join('slabbe','kolakoski_word_pyx.pyx')],),
        Extension('slabbe.mult_cont_frac_pyx',
            sources = [path.join('slabbe','mult_cont_frac_pyx.pyx')],
            include_dirs=sage_include_directories()),
        Extension('slabbe.diophantine_approx_pyx',
            sources = [path.join('slabbe','diophantine_approx_pyx.pyx')],
            include_dirs=sage_include_directories())]

# try to cythonize the cython modules, but avoid failing when it fails
# Often sage on conda or sage on ArchLinux does not have a working cython
# Users most probably just want to use the Python modules, so let's ignore
# the cython modules within slabbe
def try_cythonize_ext_module():
    try:
        return cythonize(ext_modules)
    except:
        print("Problem when calling cythonize(ext_modules) in slabbe package.")
        print("Here is the traceback showing the problem:")
        print("--- START OF TRACEBACK ---")
        import traceback
        traceback.print_exc()
        print("--- END OF TRACEBACK ---")
        print("The slabbe package will be installed without its cython modules")
        return []

setup(
    ext_modules=try_cythonize_ext_module()
)
