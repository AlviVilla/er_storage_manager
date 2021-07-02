from json import load, dump
import os
import logging
dir_path = os.path.dirname(os.path.realpath(__file__))

CONFIG_FILE = os.path.join(dir_path, "/config/config.json")

def load_config() -> dict:
    """
    Parses and returns the config file

    Returns: dict
    """
    config = {}
    print(CONFIG_FILE)
    with open(CONFIG_FILE) as j:
        config = load(j)

    return config


def save_config(data: dict):
    """
    Saves updated config file
    """
    with open(CONFIG_FILE, 'w') as j:
        dump(data,j)
