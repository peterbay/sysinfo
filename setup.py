#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import re

from distutils.core import setup
from pathlib import Path
from setuptools import find_packages, setup

def find_version(fname):
    """Attempts to find the version number in the file names fname.
    Raises RuntimeError if not found.
    """
    version = ""
    with open(fname, "r") as fp:
        reg = re.compile(r'__version__ = [\'"]([^\'"]*)[\'"]')
        for line in fp:
            m = reg.match(line)
            if m:
                version = m.group(1)
                break
    if not version:
        raise RuntimeError("Cannot find version information")
    return version


def requirements(fname):
    path = Path(fname)

    if not path.exists():
        return []

    return path.read_text().splitlines()


# We use the version to construct the DOWNLOAD_URL.
VERSION = find_version("__init__.py")

# URL to the repository on Github.
REPO_URL = 'https://github.com/peterbay/sysinfo'

# Github will generate a tarball as long as you tag your releases, so don't
# forget to tag!
DOWNLOAD_URL = ''.join((REPO_URL, '/tarball/release/', VERSION))

INSTALL_REQUIRES = requirements("requirements.txt")
EXTRAS_REQUIRE = {
    "test": requirements("requirements-dev.txt"),
}

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

ROOT = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(ROOT, "README.md"), encoding="utf-8") as f:
    readme = f.read()

setup(
    name="sysinfo",
    version=VERSION,
    description="sysinfo - Python based scripts for obtaining system information from Linux.",
    long_description=readme,
    author="Petr Vavrin",
    author_email="pvavrin@gmail.com",
    url=DOWNLOAD_URL,
    license='GNU GPLv3',
    classifiers=[
        'License :: GNU GPLv3',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.9',
    ],
    package_dir={"": "."},
    packages=find_packages(),
    install_requires=INSTALL_REQUIRES,
    include_package_data=True,
    extras_require=EXTRAS_REQUIRE,
    python_requires=">=3.9",
    py_modules=['sysinfo'],
)
