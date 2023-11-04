import os

basedir = os.path.abspath(os.path.dirname(__file__))


class BaseConfig: 
    DEFAULT_CURRENCY = {
        "currencies": {
            "TWD": {
                "TWD": 1,
                "JPY": 3.669,
                "USD": 0.03281
            },
            "JPY": {
                "TWD": 0.26956,
                "JPY": 1,
                "USD": 0.00885
            },
            "USD": {
                "TWD": 30.444,
                "JPY": 111.801,
                "USD": 1
            }
        }
    }

class DevelopmentConfig(BaseConfig):
    DEBUG = True
    CURRENCY_MODE = False




class TestingConfig(BaseConfig):
    TESTING = True
    CURRENCY_MODE = False
config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
}
