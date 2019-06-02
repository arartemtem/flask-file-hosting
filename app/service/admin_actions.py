import time
import random
import string

from flask_login import current_user
from flask import flash, redirect, url_for

from app import db
from app.models import User, File
from app.service.file_actions import FileActions


class AdminActions(FileActions):

    def admin_page(self, form):
        if current_user.is_admin:
            if form.validate_on_submit():
                sharelink = self._generate_sharelink()
                user = User(username=form.username.data, is_admin=form.is_admin.data,
                            sharelink=sharelink)
                user.set_password(form.password.data)
                db.session.add(user)
                db.session.commit()
                flash('User added', 'success')
                return redirect(url_for('admin_page'))
        else:
            return redirect(url_for('user_files'))
        return None

    def delete_user(self, user_id):
        if current_user.is_admin:
            user = User.query.filter_by(id=user_id).first()
            files = File.query.filter_by(user_id=user.id).all()
            for file in files:
                self.delete_file(file)
            user = User.query.filter_by(id=user_id).first()
            db.session.delete(user)
            db.session.commit()
            flash('User deleted', 'warning')
            return redirect(url_for('admin_page'))
        else:
            return redirect(url_for('files'))

    def _generate_sharelink(self):
        chars = string.ascii_lowercase + string.digits
        random_str = ''.join(random.choice(chars) for _ in range(10))
        time_str = str(time.time()).split('.')[0]
        return random_str + time_str

    def _delete_user_files(self, user_id):
        File.query.filter_by(user_id=user_id).delete()
        db.session.commit()
