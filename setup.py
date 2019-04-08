#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from __future__ import with_statement

try:
    from setuptools import setup, find_packages
except ImportError:
    from distutils.core import setup, find_packages


import grafana_inviter

with open("README.md", "r") as fh:
    readme = fh.read()

setup(
    name="grafana-inviter",
    version=grafana_inviter.__version__,
    author=grafana_inviter.__author__,
    author_email=grafana_inviter.__author_mail__,
    description=grafana_inviter.__description__,
    long_description=readme,
    long_description_content_type='text/markdown',
    url=("https://github.com/tomtom-international/grafana-inviter"),
    packages=["grafana_inviter"],
    python_requires=">3.5",
    install_requires=[
        "ldap3>=2.6,<3",
        "requests>=2.16.0,<3",
        "anyconfig>=0.9.8,<1",
        "jsonschema>=3.0.1,<4"
    ],
    setup_requires=["pytest-runner>=4.2,<5"],
    tests_require=[
        "coverage>=4.5,<5"
        "pytest>=4.1,<5",
        "pytest-cov>=2.6,<3"
    ],
    entry_points="""
[console_scripts]
grafana-inviter = grafana_inviter.cli:main
""",
    dependency_links=[],
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        "Environment :: Console",
        "Operating System :: OS Independent"
    ],
    license=grafana_inviter.__license__,
    zip_safe=False,
)
