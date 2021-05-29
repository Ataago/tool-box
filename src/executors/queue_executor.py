# !/usr/bin/env python3
# encoding: utf-8

"""
    This is a basic python Queue executor for Queueing your commands using file system.
    User can use this to run multiple scripts.

    Usage:
        1. Run Queue 24/7 by:
            $python3 -m src.executors.queue_executor --queue <queue_name> --pool <pool_size>
            NOTE:
                Make sure to run this from the root of the project from where all the commands scheduled would run as well.

        2. Enqueue commands from your other script:
            my_queue = QueueExecutor('my_queue')
            my_queue.enqueue(['python3 -m src.my_script'])
"""

import logging
import argparse
from src.utils.setup_logger import setup_logger
from time import sleep
import multiprocessing
from subprocess import Popen, PIPE
from datetime import datetime
from configs.conf import __WORKSPACE__
from src.utils.file_handlers import save_file, read_file
from src.utils.json_util import save_json, read_json


__author__ = 'Mohammed Ataaur Rahaman'


__QUEUE_DIR__ = __WORKSPACE__ / 'queues'
__QUEUE_NAME__ = 'Ataa_queue'
__POOL__ = 2


dt = datetime.now().strftime("%Y%m%d%H%M%S")
setup_logger(
    filename=f'queue_{dt}.log',
    # filename=f'queue_TEST.log',
    filemode='a',
    level=logging.INFO
)
log = logging.getLogger(__name__)


class QueueExecutor:

    def __init__(self, queue_name, pool=None):
        self.queue = __QUEUE_DIR__ / queue_name / 'queue'
        self.completed = __QUEUE_DIR__ / queue_name / 'completed'
        self.latest_pool = __QUEUE_DIR__ / queue_name / 'latest_pool.json'

        self.pool_file = __QUEUE_DIR__ / queue_name / 'pool_size.json'
        if pool:
            self.save_pool(pool)

    def save_pool(self, pool):
        save_json(self.pool_file, data={"pool":pool})

    def get_pool_size(self):
        return read_json(self.pool_file)['pool']

    def read_queue(self):
        files = list(self.queue.glob('*'))
        files = [int(file.name) for file in files if files]
        return sorted(files) if files else None

    def enqueue(self, commands):
        queue = self.read_queue()
        idx = -1 if not queue else queue[-1]
        for command in commands:
            idx += 1
            save_file(file_path=self.queue / str(idx), content=command)
        log.info(f"Enqueued {len(commands)} commands.")
        log.debug(f"Enqueued commands: {commands}")

    def dequeue(self, queue):
        for idx in queue:
            path = self.queue / str(idx)
            path.unlink()
        log.info(f"Dequeued {len(queue)} commands.")

    def mark_in_process(self, commands, queue):
        content = {idx:cmd for idx, cmd in zip(queue, commands)}
        save_json(file_path=self.latest_pool, data=content)

    def mark_as_completed(self, idx, cmd, status, output=None, err=None):
        """
        Save the metadata for a cmd in an JSON file
        :param idx: Integer index of the command
        :param cmd: String cmd
        :param output:String Output (if Any)
        :param err: String Error (if any)
        :param status: Boolean Status
        """
        try:
            content = {
                'command': cmd,
                'status': status,
                'output': output if output != '' else None,
                'error': err if err != '' else None
            }
            save_json(
                file_path=self.completed / '{}_{}_completed.json'.format(datetime.now().strftime("%Y%m%d%H%M%S"), idx),
                data=content
            )

        except Exception as err:
            log.warning(f'Error in storing status of cmd {cmd}: {err}')
            log.info(f'Command Status: {cmd}')

    def execute_command(self, idx, cmd):
        """
        A simple python function to run a command
        :param idx: integer Index
        :param cmd: command string
        :return: (idx, cmd, Status, Output String, Error String)
        """
        status = False
        output_str = ''
        error_str = ''
        try:
            log.info(f'Running command {idx}: {cmd}')
            cmd_out, cmd_err = Popen(
                cmd, stdout=PIPE, stderr=PIPE, shell=True
            ).communicate()

            error_str = cmd_err.decode("utf-8")
            output_str = cmd_out.decode("utf-8")
            status = True if error_str == '' else False

        except Exception as err:
            log.error(f'Command failed: {err}')

        finally:
            log.info(f"Command executed {idx}: {cmd}")
            self.mark_as_completed(idx=idx, cmd=cmd, status=status, output=output_str, err=error_str)
            self.dequeue([idx])

    def run(self):
        log.info(f"Starting Queue: {self.queue.parent.name}")

        while True:
            log.debug(f"Refreshing queue.")
            queue = self.read_queue()

            if queue:
                commands = [(idx, read_file(self.queue / str(idx))) for idx in queue]
                self.mark_in_process(commands, queue)

                log.info(f"Pooling {len(commands)} commands.")
                log.debug(f"Pooling commands: {commands}")
                worker_pool = multiprocessing.Pool(self.get_pool_size())
                worker_pool.starmap(func=self.execute_command, iterable=commands, chunksize=1)
                worker_pool.close()
                worker_pool.join()

                queue = self.read_queue()
                if not queue:
                    log.info(f"Queue is Empty. Enqueue more commands to execute..")

            sleep(2)


def get_args():
    """
    Get args when running with command line interface
    """
    # Default arguments
    arg_parser = argparse.ArgumentParser()
    arg_parser.version = '1.0.0'

    arg_parser.add_argument('-q', '--queue', action='store', type=str, required=True, help='Name of the Queue.')
    arg_parser.add_argument('-p', '--pool', action='store', type=int, required=True, help='Size of the Pool.')

    # Parse arguments
    args = arg_parser.parse_args()

    return args.queue, args.pool


if __name__ == '__main__':
    queue_name, pool = get_args()

    my_queue = QueueExecutor(queue_name, pool)
    my_queue.run()
