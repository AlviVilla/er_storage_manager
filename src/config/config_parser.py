from json import load, dump
import os
import logging



CONFIG_FILE = "config.json"

def load_config() -> dict:
    """
    Parses and returns the config file

    Returns: dict
    """
    config = {}
    dir_path = os.path.dirname(os.path.realpath(__file__))
    path= os.path.join(dir_path, CONFIG_FILE)
    with open(path) as j:
        config = load(j)

    return config


def save_config(data: dict):
    """
    Saves updated config file
    """
    dir_path = os.path.dirname(os.path.realpath(__file__))
    path= os.path.join(dir_path, CONFIG_FILE)
    with open(path, 'w') as j:
        dump(data,j)
