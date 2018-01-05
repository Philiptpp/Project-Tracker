class Config():
    DEBUG = False
    TESTING = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///res/test.db'
    SECRET_KEY = 'TheQuickBrownFoxJumpsOverTheLazyDog'


class Production(Config):
    DATABASE_URI = 'sqlite:///res/master.db'


class Development(Config):
    DEBUG = True
    TEMPLATES_AUTO_RELOAD = True
