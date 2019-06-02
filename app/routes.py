import datetime

import pytz
from flask import render_template, request, flash, redirect, url_for
from flask_login import logout_user, current_user, login_required

from app import app
from app.forms import LoginForm, UploadForm, AddUserForm, SearchForm, ChangePasswordForm
from app.models import User, File
from app.service.file_actions import FileActions
from app.service.user_actions import UserActions
from app.service.admin_actions import AdminActions


@app.route('/admin_page', methods=['GET', 'POST'])
@login_required
def admin_page():
    form = AddUserForm()
    admin_page = AdminActions().admin_page(form)
    users = User.query.all()
    return admin_page or render_template('admin.html', title='Admin', form=form, users=users)


@app.route('/delete/<file_id>')
@login_required
def delete(file_id):
    file = File.query.filter_by(id=file_id).first()
    user_id = file.user_id
    if current_user.id == user_id:
        return FileActions().delete_file(file)
    else:
        return flash('Error', 'error')


@app.route('/admin_page/delete_user/<user_id>')
@login_required
def delete_user(user_id):
    if current_user.is_admin:
        AdminActions().delete_user(user_id)
        return redirect(url_for('admin_page'))
    else:
        return redirect(url_for('user_files'))


@app.route('/download/<file_id>')
def download(file_id):
    return FileActions().download_file(file_id)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    user_login = UserActions().login(form)
    return user_login or render_template('login.html', title='Sign In', form=form)


@app.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
    form = ChangePasswordForm()
    timezone = User.query.filter_by(id=current_user.id).first().timezone
    if form.validate_on_submit():
        UserActions().change_password(current_user.id, form.old_password.data, form.password.data)
    return render_template('settings.html', title='Admin', timezones=pytz.common_timezones, user_timezone=timezone,
                           form=form)


@app.route('/settings/set_timezone/<timezone>')
@login_required
def set_timezone(timezone):
    return UserActions().set_timezone(current_user.id, timezone)


@app.route('/shared_files/<share_link>')
def shared_files(share_link):
    user = User.query.filter_by(sharelink=share_link).first()
    files = File.query.filter_by(user_id=user.id, is_shared=True)
    return render_template('shared_files.html', files=files)


@app.route('/share')
@login_required
def share_files_list():
    shared_files = File.query.filter_by(user_id=current_user.id, is_shared=True)
    not_shared_files = File.query.filter_by(user_id=current_user.id, is_shared=False)
    timezone = User.query.filter_by(id=current_user.id).first().timezone
    return render_template('share.html', shared_files=shared_files, not_shared_files=not_shared_files,
                           timedelta=datetime.datetime.now(pytz.timezone(f'{timezone or "UTC"}')).utcoffset())


@app.route('/start_sharing/<file_id>')
@login_required
def start_sharing(file_id):
    FileActions().sharing(current_user.id, file_id, share=True)
    return redirect(url_for('share_files_list'))


@app.route('/stop_sharing/<file_id>')
@login_required
def stop_sharing(file_id):
    FileActions().sharing(current_user.id, file_id, share=False)
    return redirect(url_for('share_files_list'))


@app.route('/upload', methods=['GET', 'POST'])
@login_required
def upload():
    form = UploadForm()
    FileActions().upload_file(request=request)
    return render_template('upload.html', form=form)


@app.route('/', methods=['GET', 'POST'])
@app.route('/files', methods=['GET', 'POST'])
@login_required
def user_files():
    form = SearchForm()
    files = FileActions().file_list(form)
    timezone = User.query.filter_by(id=current_user.id).first().timezone
    return render_template('files.html', files=files, form=form,
                           timedelta=datetime.datetime.now(pytz.timezone(f'{timezone or "UTC"}')).utcoffset())
