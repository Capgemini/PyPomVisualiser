# PyPomVisualiser

Platform independent Maven Pom structure visualiser, written in Python.

Dependencies in Maven can be difficult to resolve, this is especially true when you ask the question 'what depends on this?'. This program aims to help alleviate this issue by creating a logical tree structure from a scan of all the poms which constitute the project, and then determining reverse dependencies. 
The structure will then be output to a platform independent window for review.

The eventual aim is to add capability to manipulate the pom from the visualisation screen, certainly for simple things like version changes, if not full dependency management.

Basic Getting Started

Requirements:
  
  Python 3.4 
  
  TKinter (On APT backed linux distros this can be acquired with 'sudo apt-get install python3-tk')
  

Run using:
python pypomv.py <location of a pom>

#Package Installation instructions
cd <downloaded location>/PyPomVisualiser
Install using: python setup.py install

This may need to be run with enhanced privileges.

Can be run with pypomv.py

Will be packaged better in the future!

#Having issues with installation?
Would suggest running Python in pyenv so not to interfere with system python (https://github.com/yyuu/pyenv#installation). You will also need to install tk (sudo apt-get install tk8.6-dev) so the python built from source (using pyenv) can find the headers and compile this module.


