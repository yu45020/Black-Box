# To setup this module, run "python setup.py install" in terminal

import os
from setuptools import setup
from MplDecorator._version import __version__

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = 'MplDecorator',
    version = str(__version__),
    author = "Kuang，Hengyu",
    description = ("Decorator of matplotlib plots"),
    packages = ["MplDecorator"],
)