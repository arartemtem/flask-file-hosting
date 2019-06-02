from flask_login import login_user, current_user
from flask import request, flash, redirect, url_for
from werkzeug.urls import url_parse

from app import db
from app.models import User


class UserActions:

    def change_password(self, user_id, old_password, new_password):
        user = User.query.filter_by(id=user_id).first()
        if not user.check_password(old_password):
            flash('Invalid old password', 'danger')
            return redirect(url_for('settings'))
        else:
            user.set_password(new_password)
            db.session.commit()
            flash('Password Changed!', 'success')
            return redirect(url_for('settings'))
    
    def login(self, form):
        if current_user.is_authenticated:
            return redirect(url_for('user_files'))
        elif form.validate_on_submit():
            user = User.query.filter_by(username=form.username.data).first()
            if user is None or not user.check_password(form.password.data):
                flash('Invalid username or password', 'danger')
                return redirect(url_for('login'))
            login_user(user, remember=form.remember_me.data)
            next_page = request.args.get('next')
            if not next_page or url_parse(next_page).netloc != '':
                next_page = url_for('user_files')
            return redirect(next_page)
        return None

    def set_timezone(self, user_id, timezone):
        timezone = timezone.replace('-', '/')
        user_row = User.query.filter_by(id=user_id).first()
        user_row.timezone = timezone
        db.session.commit()
        flash('Timezone saved', 'success')
        return redirect(url_for('settings'))
