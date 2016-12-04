# -*- coding: utf-8 -*-
"""
Created on Thu Dec  1 21:41:14 2016

@author: Tom Blanchet
"""

from setuptools import setup, find_packages

from codecs import open
from os import path

README_FILE = 'README.md'
HERE = path.abspath(path.dirname(__file__))

with open(path.join(HERE, README_FILE), encoding='utf-8') as f:
    long_description = f.read()
    
setup(
    name='lwf_test',

    version='0.1a0',

    description='A simple library for unit testing python code',
    long_description=long_description,

    url='https://github.com/FrogBomb/lwf_test',

    author='Tom Blanchet',
    author_email='tlblanchet@gmail.com',
    license='MIT',

    classifiers=[
        'Development Status :: 3 - Alpha',

        'Intended Audience :: Developers',
        'Topic :: Software Development :: Testing Tools',

        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.5',
    ],
    keywords='unittest test lightweight development',
    packages=['lwf_test', 'lwf_test.package_tests'],
    package_data={'lwf_test': '*.txt'},
#    package_dir = {'lwf_test':'lwf_test'},
    entry_points={
        'console_scripts': [
            'lwf_test=lwf_test.__main__:main'
        ],
    },
)