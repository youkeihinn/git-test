#!/usr/bin/env python
#coding:utf-8

from setuptools import setup,find_packages

setup(
    name = 'flaskr',
    packages = find_packages(),
    include_package_data = True,
    install_requires = ['flask',],
    setup_requires=['pytest-runner',],
    tests_require=['pytest',],
)
