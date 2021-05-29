# !/usr/bin/env python3
# encoding: utf-8

"""
Sample file
"""

import logging as log
from src.utils.setup_logger import setup_logger
from time import sleep

from datetime import datetime



__author__ = 'Mohammed Ataaur Rahaman'





if __name__ == '__main__':
    dt = datetime.now().strftime("%Y%m%d%H%M%S")

    setup_logger(
        # filename=f'queue_{dt}.log',
        filename=f'ataa.log',
        filemode='w+',
        level=log.INFO
    )
    sleep(2)
    log.info(f"My log file triggered {dt}")