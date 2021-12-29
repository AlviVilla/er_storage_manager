from json import load, dump, loads
import os
import logging



CONFIG_FILE = "config.json"


def load_config(path: str) -> dict:

    """
    Parses and returns the config file

    Returns: dict
    """
    config = {}
    with open(path) as j:
        config = load(j)

    return config


def save_config(path: str, data: dict):
    """
    Saves updated config file
    """
    dir_path = os.path.dirname(os.path.realpath(__file__))
    path= os.path.join(dir_path, CONFIG_FILE)
    with open(path, 'w') as j:
        dump(data,j)


def get_config():

    """
    Loads entire configuration onto memory
    """
    env_vars = [
    "HOST",
    "PORT",
    "DEBUG_MODE",
    "TAG_LIST"]

    dir_path = os.path.dirname(os.path.realpath(__file__))
    path= os.path.join(dir_path, CONFIG_FILE)

    use_env_var = True

    for env_var in env_vars:
        if env_var not in os.environ:
            use_env_var = False

    g_config = {}
    # Global config objects
    if use_env_var is False:
        g_config = load_config(path)
    else:
        for env_var in env_vars:
            if "true" in os.environ[env_var].replace('"', ''):
                g_config[env_var.lower()] = True
            elif "false" in os.environ[env_var].replace('"', ''):
                g_config[env_var.lower()] = False
            else:
                g_config[env_var.lower()] = os.environ[env_var].replace('"', '')
    if isinstance(g_config["tag_list"], str):
        a = loads(g_config["tag_list"][3:].replace('\'', '"'))
        g_config["tag_list"] = a
    save_config(path, g_config)
    return g_config