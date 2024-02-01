from instance.config import MONGO_URI


class Config:
    """
    General configuration.
    """
    MONGO_URI = MONGO_URI
    DEBUG = False


class DevelopmentConfig(Config):
    """
    Development configuration.
    """
    DEBUG = True


class ProductionConfig(Config):
    """
    Production configuration.
    """
    WORKERS = 4


class TestingConfig(Config):
    """
    Testing configuration.
    """
    DEBUG = True
    TESTING = True
