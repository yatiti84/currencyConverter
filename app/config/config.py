import os

basedir = os.path.abspath(os.path.dirname(__file__))


class BaseConfig:
    IS_DEFAULT_CURRENCY_DATA = True


class DevelopmentConfig(BaseConfig):
    DEBUG = True


class TestingConfig(BaseConfig):
    TESTING = True


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
}
