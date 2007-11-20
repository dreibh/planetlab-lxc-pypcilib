#!/usr/bin/env python

from distutils.core import setup, Extension

setup(name='pypciscan',
      version='0.1',
      description='PCI scanning from Python',
      author='Daniel Hokka Zakrisson',
      author_email='daniel@hozac.com',
      packages=['pypcimap'],
      ext_modules=[Extension('pypciscan', ['pypciscan.c'],
			     libraries=['pci', 'z'])],
     )
