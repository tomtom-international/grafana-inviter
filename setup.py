#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from __future__ import with_statement

try:
    from setuptools import setup, find_packages
except ImportError:
    from distutils.core import setup, find_packages

import grafana_inviter


with open("README.md") as readme_file:
    readme = readme_file.read()

with open("CHANGELOG.md") as changelog_file:
    changelog = changelog_file.read()

requirements = ["python-ldap", "requests", "anyconfig", "jsonschema"]

setup_requirements = ["pytest-runner",]

test_requirements = ["pytest", "pytest-cov", "coverage",]

setup(
    author=grafana_inviter.__author__,
    author_email=grafana_inviter.__email__,
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Natural Language :: English",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
    ],
    description="Python module and script to invite people fetched from LDAP to Grafana",
    entry_points={
        "console_scripts": [
            "grafana-inviter=grafana_inviter.cli:main",
        ],
    },
    install_requires=requirements,
    license="Apache Software License 2.0",
    long_description=readme + "\n\n" + changelog,
    long_description_content_type="text/markdown",
    include_package_data=True,
    keywords="grafana_inviter",
    name="grafana-inviter",
    packages=find_packages(include=["grafana_inviter"]),
    setup_requires=setup_requirements,
    test_suite="tests",
    tests_require=test_requirements,
    url="https://github.com/tomtom-international/grafana-inviter",
    version=grafana_inviter.__version__,
    zip_safe=False,
)
