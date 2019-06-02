import os
from datetime import datetime

import hashlib
from flask_login import login_user, logout_user, current_user, login_required
from flask import render_template, request, flash, redirect, url_for, send_file
from sqlalchemy import desc
from werkzeug.urls import url_parse

from app import app, db, functions
from app.models import User, File


class UserActions:
    
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

    def change_password(self, form):
        if form.validate_on_submit():
            user = User.query.filter_by(id=current_user.id).first()
            if not user.check_password(form.old_password.data):
                flash('Invalid old password', 'danger')
                return redirect(url_for('settings'))
            else:
                user.set_password(form.password.data)
                db.session.commit()
                flash('Password Changed!', 'success')
                return redirect(url_for('settings'))

    def set_timezone(self, timezone):
        timezone = timezone.replace('-', '/')
        user_row = User.query.filter_by(id=current_user.id).first()
        user_row.timezone = timezone
        db.session.commit()
        flash('Timezone saved', 'success')
        return redirect(url_for('settings'))
