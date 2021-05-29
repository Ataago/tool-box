# !/usr/bin/env python3
# encoding: utf-8

"""
    Main Script to generate standard ASTs.
"""

import sys
import logging as log

from configs import conf_logger as LOGGER

__author__ = "Mohammed Ataaur Rahaman"


def setup_logger(
    filename=None,
    level=LOGGER.__DEFAULT_LEVEL__,
    filemode=LOGGER.__DEFAULT_FILEMODE__,
    format=LOGGER.__DEFAULT_FORMAT__,
    sysout=LOGGER.__LOG_SYS_OUT__,
):
    """
    Standard logger setup method.

    @param filename: Name of the file which gets stored in default log folder.
    @param level: Level of logging
    @param filemode: Filemode for logging file
    @param format: Format of logging text
    @param sysout: Boolean to log on sys out if true
    @return:
    """

    if sysout:
        log.basicConfig(stream=sys.stdout, level=level, format=format)

    else:
        # Create logger folder if doesn't exists
        LOGGER.__LOGS_FOLDER__.mkdir(parents=True, exist_ok=True)
        if not filename:
            raise Exception("Please provide logging file name.")

        filename = LOGGER.__LOGS_FOLDER__ / filename
        log.basicConfig(
            filename=filename, level=level, filemode=filemode, format=format
        )
