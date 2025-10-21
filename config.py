import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'halfbakery.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    PROJECTS_DIR = os.path.join(basedir, 'projects')
