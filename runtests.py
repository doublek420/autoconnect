#!/usr/bin/env python
#
# Use nosetests to run the acceptance tests for this project.
#
# This script sets up the paths to find packages (see package_paths)
# and limits the test discovery to only the listed set of locations
# (see test_paths).
#
# Oisin Mulvihill
# 2007-07-10
#
import os
import sys
import nose
import logging


sys.path.extend(['./lib'])

result = nose.core.TestProgram().success
nose.result.end_capture()

