# PyPomVisualiser

Platform independent Maven Pom structure visualiser, written in Python.

Dependencies in Maven can be difficult to resolve, this is especially true when you ask the question 'what depends on this?'. This program aims to help alleviate this issue by creating a logical tree structure from a scan of all the poms which constitute the project, and then determining reverse dependencies. 
The structure will then be output to a platform independent window for review.

The eventual aim is to add capability to manipulate the pom from the visualisation screen, certainly for simple things like version changes, if not full dependency management.

Getting Started

Requirements:
  Python 3
  TKinter (On APT backed linux distros this can be acquired with 'sudo apt-get install python3-tk')

Run using:
Python3 run.py <location of a pom>

Will be packaged better in the future!
