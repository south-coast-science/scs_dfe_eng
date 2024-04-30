#!/usr/bin/env python3

"""
Created on 4 Sep 2020
Updated 23 Mar 2021

@author: Jade Page (jade.page@southcoastscience.com)

https://packaging.python.org/tutorials/packaging-projects/
https://packaging.python.org/guides/single-sourcing-package-version/
"""

import codecs
import os

from setuptools import setup, find_packages


# --------------------------------------------------------------------------------------------------------------------

def read(rel_path):
    here = str(os.path.abspath(os.path.dirname(__file__)))
    with codecs.open(os.path.join(here, rel_path)) as fp:
        return fp.read()


def get_version(rel_path):
    for line in read(rel_path).splitlines():
        if line.startswith('__version__'):
            return line.split("'")[1]
    else:
        raise RuntimeError("Unable to find version string.")


# --------------------------------------------------------------------------------------------------------------------

with open('requirements.txt') as req_txt:
    required = [line for line in req_txt.read().splitlines() if line]


setup(
    name='scs_dfe_eng',
    version=get_version("src/scs_dfe/__init__.py"),
    description='Environmental sampling abstractions for the South Coast Science Alpha _ Eng. digital front-end. ',
    author='South Coast Science',
    author_email='contact@southcoastscience.com',
    url='https://github.com/south-coast-science/scs_dfe_eng',
    package_dir={'': 'src'},
    packages=find_packages('src'),
    classifiers=[
        'Development Status :: 4 - Beta',
        'Operating System :: POSIX',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    install_requires=required,
    platforms=['any'],
    python_requires=">=3.3",
)
