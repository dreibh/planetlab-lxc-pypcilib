#!/usr/bin/env python

from distutils.core import setup, Extension

setup(name='pypciscan',
      version='0.2',
      description='PCI scanning from Python',
      author='Daniel Hokka Zakrisson and Stephen Soltesz',
      author_email='daniel@hozac.com',
      py_modules=['pypcimap', 'pypci'],
     )
