# !/usr/bin/env python3
# encoding: utf-8

"""
This is a basic python executor for BOML FLows.
User can use this to run multiple flows.
"""

from src.executors.queue_executor import QueueExecutor
import logging as log
from src.utils.setup_logger import setup_logger
from time import sleep
import multiprocessing
from subprocess import Popen, PIPE
from datetime import datetime
from configs.conf import __WORKSPACE__
from configs.conf_logger import __DEFAULT_LEVEL__, __DEFAULT_FORMAT__, __DEFAULT_FILEMODE__
from src.utils.file_handlers import save_file
import argparse
from src.utils.json_util import read_json


__author__ = 'Mohammed Ataaur Rahaman'


__QUEUE_DIR__ = __WORKSPACE__ / 'queues'



if __name__ == '__main__':
    dt = datetime.now().strftime("%Y%m%d%H%M%S")

    setup_logger(
        # filename=f'queue_{dt}.log',
        filename=f'sample_queue.log',
        filemode='w+',
        level=log.INFO
    )

    my_queue = QueueExecutor('my_queue', pool=2)
    # my_queue.enqueue(['python3 -m src.executors.flow', 'python3 -m src.executors.flow1'])
    my_queue.enqueue(['python3 -m src.executors.flow']*10)
