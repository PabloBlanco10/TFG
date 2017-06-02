from distutils.core import setup, Extension
import numpy

module1 = Extension('funcionesC', sources = ['funcionesC.c'], include_dirs=[numpy.get_include()])

setup (name = 'FuncionesC',
        version = '1.0',
        description = 'oct2015',
        ext_modules = [module1])
