# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

try:
    long_description = open("README.md").read()
except IOError:
    long_description = ""

setup(
    name="breeze-rect",
    version="0.1.0",
    description="A breeze plugin for the Rect programming language",
    license="MIT",
    package_dir = {"": "src"},
    author_email='mauro.balades@tutanota.com',
    author="mauro-balades",
    packages=find_packages(where="src"),
    install_requires=["breeze"],
    long_description=long_description,
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.8",
    ]
)
