import ez_setup
ez_setup.use_setuptools()

from setuptools import setup, find_packages

setup(
    # Application name:
    name="PyPomVisualiser",

    # Version number (initial):
    version="0.7.0",

    # Application author details:
    author="William Moorhouse",
    author_email="w-mg-moorhouse@gmail.com",
    scripts = ["pypomv.py"],
    # Packages
    packages = find_packages(),

    # Include additional files into the package
    include_package_data=True,

    # Details
    url="https://github.com/w-mg-moorhouse/PyPomVisualiser",

    #
    license="LICENSE",
    description="Maven Pom Visualisation tool, written in Python(obviously).",

    # long_description=open("README.txt").read(),

    # Dependent packages (distributions)
    install_requires=[
        #"tkinter"
    ],
)
