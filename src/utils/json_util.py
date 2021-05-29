#!/usr/bin/env python3
# encoding: utf-8

"""
    Json files utility functions
"""

import json


__author__ = "Mohammed Ataaur Rahaman"


def save_json(file_path, data):
    """
    Saves data in json format at file_path.

    :param file_path(pathlib Path): Absolute json file path to save json
    :param data(dict): data in dictionary format
    """
    try:
        file_path.parent.mkdir(parents=True, exist_ok=True)
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
    except Exception as err:
        raise Exception(err)

def read_json(file_path):
    """
    Reads the file_path and returns the data.

    :param file_path(pathlib Path): Absolute path to json file
    :return: data in dictionary format
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as err:
        raise Exception(err)
