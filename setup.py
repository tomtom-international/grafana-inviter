from __future__ import with_statement

from setuptools import setup, find_packages

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
    url=("https://github.com/tomtom-international/grafana-inviter"),
    packages=["grafana_inviter"],
    python_requires=">3.5",
    install_requires=[
        "python-ldap>=3.1.0,<4",
        "requests>=2.16.0,<3",
        "anyconfig>=0.9.8,<1"
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
        "Programming Language :: Python :: 3",
        "Intended Audience :: Developers",
        "Environment :: Console",
        "Operating System :: OS Independent",
    ],
    license=grafana_inviter.__license__,
    zip_safe=False,
)
