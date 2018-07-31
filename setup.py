#!/usr/bin/env python

from setuptools import setup, find_packages


setup(
    name = 'pw1-client',
    version = '1.0',
    author = 'Rodrigo Cacilhas',
    author_email = 'rodrigo.cacilhas@nexaas.com',
    description = '',
    license = 'Proprietary License',
    keywords = 'passaporte-web oauth',
    url = '',
    packages = find_packages(exclude=('tests', 'tests.*')),
    long_description = '',
    test_suite = 'tests',
    install_requires = [
        'requests>=2.19.0',
    ],
    tests_require = [
        'pycodestyle>=2.3.1',
        'pylint>=1.8.2',
        'vcrpy>=1.13.0',
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'License :: Other/Proprietary License',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3 :: Only',
        'Topic :: Utilities',
    ],
)
