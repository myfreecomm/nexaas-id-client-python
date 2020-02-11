#!/usr/bin/env python

from pathlib import Path
from setuptools import setup, find_packages

with (Path(__file__).parent / 'README.md').open() as fp:
    long_description = fp.read()


setup(
    name='nexaas-id-client',
    version='1.0.1',
    author='Rodrigo Cacilhas',
    author_email='rodrigo.cacilhas@nexaas.com',
    description='Nexaas ID Python client',
    long_description=long_description,
    long_description_content_type='text/markdown',
    license='Proprietary License',
    keywords='nexaas-id oauth',
    url='https://github.com/myfreecomm/nexaas-id-client-python',
    packages=find_packages(exclude=('tests', 'tests.*')),
    test_suite='tests',
    install_requires=[
        'python-dateutil>=2.7.0',
        'requests>=2.19.0',
    ],
    tests_require=[
        'django==2.2.10',
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
