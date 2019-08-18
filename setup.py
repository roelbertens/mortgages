#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

import setuptools

with open("README.md") as readme_file:
    readme = readme_file.read()

setuptools.setup(
    name="mortgage",
    author="Roel Bertens",
    author_email="roelbertens@godatadriven.com",
    description="Compute and compare different mortgages.",
    install_requires=['numpy', 'scikit-learn', 'matplotlib'],
)
