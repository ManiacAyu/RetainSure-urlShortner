# This file makes the app directory a Python package
from flask import Flask

def create_app():
    app = Flask(__name__)
    return app
