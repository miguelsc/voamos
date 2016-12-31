#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [
    'Click>=6.0',
    # TODO: put package requirements here
]

test_requirements = [
    # TODO: put package test requirements here
]

setup(
    name='voamos',
    version='0.1.0',
    description="Google Flights scraper",
    long_description=readme + '\n\n' + history,
    author="Miguel Coutada",
    author_email='michaelcoutada@gmail.com',
    url='https://github.com/miguelsc/voamos',
    packages=[
        'voamos',
    ],
    package_dir={'voamos': 'voamos'},
    entry_points={
        'console_scripts': [
            'voamos=voamos.cli:main'
        ]
    },
    include_package_data=True,
    install_requires=requirements,
    license="GNU GPLv3",
    zip_safe=False,
    keywords='voamos',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU GPLv3',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    test_suite='tests',
    tests_require=test_requirements
)
