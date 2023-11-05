from flask import Flask, request
from .config.config import config
from .currency import convert


def create_app(config_name):

    app = Flask(__name__)
    app.config.from_object(config[config_name])

    @app.route('/')
    def health_check():
        return 'ok'

    @app.route('/convert', methods=['GET'])
    def convert_currency():

        args = request.args
        return convert(args)

    return app
