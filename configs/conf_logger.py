#!/usr/bin/env python3
# encoding: utf-8

"""
    Config file for gumtree_client
"""

from pathlib import Path
import logging as log

from configs.conf import __WORKSPACE__


__author__ = "Mohammed Ataaur Rahaman"


__LOGS_FOLDER__ = __WORKSPACE__ / "logs"

# Logger Default parameters
__DEFAULT_LEVEL__ = log.INFO
__DEFAULT_FILEMODE__ = "w+"
__DEFAULT_FORMAT__ = '%(asctime)s : %(threadName)s:  %(levelname)s : %(' \
                       'name)s : %(filename)s : %(message)s'

# Logs on system output
__LOG_SYS_OUT__ = False
