# -*- coding: utf-8 -*-


"""setup.py: setuptools control."""


import re
from os.path import exists
from setuptools import setup


version = re.search(
    '^__version__\s*=\s*"(.*)"', open("{{AppName}}/{{AppName}}.py").read(), re.M
).group(1)

if exists("README.md"):
    with open("README.md", "rb") as f:
        long_descr = f.read().decode("utf-8")
else:
    long_descr = ("{{AppDescription}}",)

setup(
    name="cmdline-{{AppName}}",
    packages=["{{AppName}}"],
    entry_points={"console_scripts": ["{{AppName}} = {{AppName}}.{{AppName}}:main"]},
    version=version,
    description="{{AppDescription}}",
    long_description=long_descr,
)
