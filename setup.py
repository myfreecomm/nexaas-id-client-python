#!/usr/bin/env python

from setuptools import setup, find_packages


setup(
    name = 'nexaas_id_client',
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
        'python-dateutil>=2.7.0',
        'requests>=2.19.0',
    ],
    tests_require=[
        'django==2.0.0',
        'Flask==1.0.2',
        'pycodestyle==2.4.0',
        'pylint==2.0.1',
        'vcrpy==1.13.0',
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'License :: Other/Proprietary License',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3 :: Only',
        'Topic :: Utilities',
    ],
)
