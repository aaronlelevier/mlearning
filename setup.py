#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import re

from setuptools import find_packages, setup


def get_version(package):
    """
    Return package version as listed in `__version__` in `init.py`.
    """
    init_py = open(os.path.join(package, '__init__.py')).read()
    return re.search("__version__ = ['\"]([^'\"]+)['\"]", init_py).group(1)


version = get_version('mlearning')


setup(
    name='mlearning',
    version=version,
    url='https://github.com/aaronlelevier/mlearning',
    license='MIT',
    description="Code repo for general machine learning code that doesn't belong to any one repo or model in particular",
    author='Aaron Lelevier',
    author_email='aaron.lelevier@gmail.com',
    packages=find_packages(exclude=['tests*']),
    include_package_data=True,
    install_requires=[
        'numpy',
        'matplotlib',
        'opencv-python',
    ],
    python_requires=">=3.6",
    zip_safe=False,
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Topic :: Internet :: WWW/HTTP',
    ]
)
