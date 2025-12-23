#!/usr/bin/env python3

###############################################################################
# Sunswift High Level DDS Package generator
# Version: V0.1
# Date: 24/12/2025
# Author: Ryan Wong
#
# Creates a new package according to this structure in the directory which you
# run this script from
# 
# <package_name>/
#     src/
#     include/
#     config/
#     launch/
#     logs/
#     CMakeLists.txt
#     README.md
#
# src -> all your .cpp files
# include -> all your .hpp files
# config -> json files (probably) for node configs + params + choice of launch file
# launch -> containing one or more launch files
# logs -> directory for node output logs
# 
# Usage in directory you want to create pkg in:
#   
###############################################################################

print("Hello world")