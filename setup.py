#!/usr/bin/env python

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name                          = 'izi',
    version                       = '0.0.6',
    py_modules                    = ['izi'],
    include_package_data          = True,
    description                   = 'Python CLI app to manage DNX Stacks and Modules',
    license                       = 'Apache 2.0',
    url                           = 'https://github.com/DNXLabs/izi',
    long_description              = long_description,
    long_description_content_type = "text/markdown",
    author                        = 'DNX Solutions',
    author_email                  = 'contact@dnx.solutions',
    classifiers                   = [
        "Programming Language :: Python",
        "Programming Language :: Python :: 3"
    ],
    packages                      = ["izi"],
    python_requires               = '>=3.6',
    entry_points='''
        [console_scripts]
        izi=izi.__main__:main
    ''',
)