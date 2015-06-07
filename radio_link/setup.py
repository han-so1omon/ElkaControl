#!/usr/bin/env python

'''
    Setup details for ElkaControl project
'''

from distutils.core import setup
from setuptools import *

setup(name = 'ElkaControl',
      version = '1.0.0b1',
      description = 'ELKA MAV testbed suite and GUI'
      author = 'Eric Solomon, Vikram Hrishikeshavan, Ryan Duffy',
      license='beerware',
      url = https://github.com/han-so1omon/ElkaControl.git
      packages=find_packages(), 
      install_requires=[usb, pygame, serial],
      )
