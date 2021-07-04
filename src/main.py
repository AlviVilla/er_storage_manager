#!/usr/bin/env python3
import json
from random import choice
from string import ascii_lowercase
from flask import Flask
from config import config_parser
from mongo.manager import mongo_manager_bp
import os


g_config = config_parser.get_config()

# Global config objects

app = Flask(__name__)
app.secret_key = ''.join(choice(ascii_lowercase) for i in range(30)) # Random key

# Register api blueprints (module endpoints)
bp, mongo = mongo_manager_bp()
app.register_blueprint(bp)

# Register the first database bulk

dir_path = os.path.dirname(os.path.realpath(__file__))
path= os.path.join(dir_path, 'config/base.json')
with open(path) as json_file:
    data = json.load(json_file)
    mongo.insert_document(data)

app.run(
    debug=g_config["debug_mode"],
    port=g_config["port"],
    host=g_config["host"]
)