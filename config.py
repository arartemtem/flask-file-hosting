import os
basedir = os.path.abspath(os.path.dirname(__file__))
test_base_dir = f'{basedir}/tests'


class Config(object):
    UPLOAD_FOLDER = f'{basedir}/files'
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class TestConfig(object):
    UPLOAD_FOLDER = f'{basedir}/tests/files'
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'tests/test_app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
