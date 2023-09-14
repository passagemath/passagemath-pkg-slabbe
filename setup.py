#!/usr/bin/env sage-python23

from setuptools import setup, Extension
from codecs import open # To use a consistent encoding
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

# Get the long description from the README file
here = path.abspath(path.dirname(__file__))
with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(name='slabbe',
    version=open("VERSION").read().strip(),
    description="Sebastien Labbe's Research code",
    long_description=long_description,
    long_description_content_type='text/x-rst',
    classifiers=[
      # How mature is this project? Common values are
      #   3 - Alpha
      #   4 - Beta
      #   5 - Production/Stable
      'Development Status :: 4 - Beta',
      'Intended Audience :: Science/Research',
      'License :: OSI Approved :: GNU General Public License v2 or later (GPLv2+)',
      'Programming Language :: Python :: 3.7',
      'Topic :: Scientific/Engineering :: Mathematics',
    ],
    keywords='sagemath combinatorics discrete geometry symbolic dynamics',
    author='Sebastien Labbe',
    author_email='slabbe@ulg.ac.be',
    install_requires=[],
    #install_requires=['pytimeparse', 'roman'], # this creates undesirable dependencies
    #install_requires=['cython','cysignals'], # this causes update of cysignals
                                              # which forces recompilation of all cython files!
    #url='http://www.slabbe.org/Sage',
    url='http://gitlab.com/seblabbe/slabbe',
    license = "GPLv2+",
    packages=['slabbe'],
    ext_modules = try_cythonize_ext_module()
)

