# packages/backend/config.py

class Config:
    DEBUG = True
    DATABASE_URI = 'sqlite:///:memory:'

config = Config()