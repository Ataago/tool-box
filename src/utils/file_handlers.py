#!/usr/bin/env python3
# encoding: utf-8

"""
    File Handlers.
"""

import json
import csv

__author__ = "Mohammed Ataaur Rahaman"


def read_file(file_path):
    """
    Read file contents and return as string.

    :param file: Absolute path to file.
    :return: content of the file as str.
    """
    try:
        with open(file_path, "r", encoding="utf-8", errors="replace") as f:
            return f.read()

    except Exception as e:
        raise Exception(f"Failed to load file {file_path}. Error: {e}")


def load_json(file_path):
    """
    Read file contents and return as Dictionary.
    :param file: Absolute path to file.
    :return: content of the file as Dictionary.
    """
    try:
        with open(file_path, "r") as f:
            return json.load(f)

    except Exception as e:
        raise Exception(f"Failed to load file {file_path}. Error: {e}")


def save_file(file_path, content, extension=None):
    """
    Saves a file.

    :param file_path(Path obj): absolute path.
    :param content(str): Content to store
    """
    file_path.parent.mkdir(parents=True, exist_ok=True)
    try:
        with open(file_path, 'w') as f:
            if extension == 'json':
                json.dump(content, f, indent=2)
            else:
                f.write(content)

    except Exception as e:
        raise Exception(f"Couldn't save file: {file_path} due to: {e}")


def save_dict_to_csv(file_path, content):
    """
    Save a list of dictionary to CSV
    :param file_path: absolute path.
    :param content: Content to store
    """
    file_path.parent.mkdir(parents=True, exist_ok=True)
    with open(file_path, "w") as f:
        writer = csv.DictWriter(f=f, fieldnames=list(content[0].keys()))
        writer.writeheader()
        writer.writerows(rowdicts=content)

def get_all_file_names(dir_path):
    """
    Recursive function to get all files paths present in
    dir_path.

    @param dir_path: Absolute path to the Directory
    @return: Set of all the file names present in dir_path
    """
    file_names = set()

    for child in dir_path.iterdir():
        if child.is_dir():
            file_names = file_names.union(get_all_file_names(child))
            continue
        if child.stem.startswith('.'):
            continue
        file_names.add(child)

    return file_names