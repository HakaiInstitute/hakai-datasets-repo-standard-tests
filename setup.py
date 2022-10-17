#!/usr/bin/env python

from distutils.core import setup

setup(
    name="hakai_data_repo_tests",
    version="1.0",
    description="Python Distribution Utilities",
    author="Jessy Barrette",
    author_email="jessy.barrette@hakai,org",
    url="https://github.com/HakaiInstitute/hakai-datasets-repo-standard-tests",
    packages=["hakai_data_repo_tests"],
    include_package_data=True,
    install_requires=["pytest", "pandas", "pyyaml"],
)
