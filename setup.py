#!/usr/bin/env python

'''
    Setup details for ElkaControl project
'''

from distutils.core import setup
from setuptools import *

setup(name='ElkaControl',
      version='1.0.0b1',
      description='ELKA MAV testbed suite and GUI',
      author='Eric Solomon',
      license='GPLv3',
      url='https://github.com/han-so1omon/ElkaControl.git',
      classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Engineers',
        'License :: OSI Approved :: GPLv3'
        'Programming Language :: Python :: 2.7',
      ],
      packages=find_packages(), 
      #TODO override this with wheeled archives
      #pip wheel -w wheels/sys_wheel_dir -r requirements.txt
      #pip install --no-index --find-links=./wheels -r requirements.txt
      install_requires=['pyusb',
          'pygame',
          'pyserial',
          'pyusb',
          'matplotlib',
          'numpy',
          'numpydoc',
          'ipython'
      ],
      )
