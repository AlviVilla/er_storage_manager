#!/usr/bin/env python3
import json
import os
import re

from random import choice
from string import ascii_lowercase
from flask import Flask

from config import config_parser
from mongo.manager import mongo_manager_bp




g_config = config_parser.load_config()

# Global config objects

app = Flask(__name__)
app.secret_key = ''.join(choice(ascii_lowercase) for i in range(30)) # Random key

# Register api blueprints (module endpoints)
bp, mongo = mongo_manager_bp()
app.register_blueprint(bp)

mongo.insert_document(name="First Article", description="This is an article, first in its species", scopes=['Article', 'Document'])
app.run(
    debug=g_config["debug_mode"],
    port=g_config["port"],
    host=g_config["host"]
)


        