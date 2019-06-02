from app import db, login
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


@login.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    is_admin = db.Column(db.Boolean)
    password_hash = db.Column(db.String(128))
    timezone = db.Column(db.String(64))
    sharelink = db.Column(db.String(64), unique=True)
    files = db.relationship('File', backref='owner', lazy='dynamic')

    def __repr__(self):
        return f'<id={self.id} username={self.username} is_admin={self.is_admin} sharelink={self.sharelink}>'

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class File(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filepath_id = db.Column(db.Integer, db.ForeignKey('file.id'))
    filename = db.Column(db.String(140))
    uploadtime = db.Column(db.DateTime)
    is_shared = db.Column(db.Boolean)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return f'<id={self.id} filename={self.filename} user_id={self.user_id}>'


class FilePath(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filepath = db.Column(db.String(140))

    def __repr__(self):
        return f'<id={self.id} filename={self.filename} user_id={self.user_id}>'
