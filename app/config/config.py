import os

basedir = os.path.abspath(os.path.dirname(__file__))


class BaseConfig:
    CURRENCY_MODE = False


class DevelopmentConfig(BaseConfig):
    DEBUG = True


class TestingConfig(BaseConfig):
    TESTING = True


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
}
