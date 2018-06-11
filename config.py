import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    UPLOAD_FOLDER = '/home/linuxlite/flask-file-hosting/files'
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    # ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
