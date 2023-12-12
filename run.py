#!/bin/env python3

from sys import argv as arguements
from os import system

parameters = ""

for arguement in arguements[ 1 : ]:
    parameters += " " + arguement

system( "/usr/src/rhenium/rhenium.py " + parameters )
