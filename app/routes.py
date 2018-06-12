import os
from flask import Flask, render_template, request, flash, redirect, url_for, send_file
from flask_login import login_user, logout_user, current_user, login_required
from app import app, db, functions
from werkzeug.utils import secure_filename
from werkzeug.urls import url_parse
from app.forms import LoginForm, UploadForm, AddUserForm
from app.models import User, File

@app.route('/upload', methods=['GET', 'POST'])
@login_required
def upload():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename 
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file:
            filename = secure_filename(file.filename)
            tmp_file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(tmp_file_path)
            md5_filename = functions.md5(filename, app.config['UPLOAD_FOLDER'])
            dir_for_file = os.path.join(app.config['UPLOAD_FOLDER'], md5_filename[0:3], md5_filename[3:6])
            os.system('mkdir -p ' + dir_for_file)     # check for the existence of a folder!
            new_filename = md5_filename[7:]
            file_path = os.path.join(dir_for_file, new_filename)
            if os.path.exists(file_path):
                file_exists = False 
                os.system('rm ' + tmp_file_path)
                filepath_list = File.query.filter_by(filepath=file_path)
                for f in filepath_list:
                    if f.user_id == current_user.id:
                        file_exists = True
                        exists_name = f.filename
                        flash('File already exists with name "' + exists_name + '"')
                        break
                if not file_exists:
                    user_file = File(filepath=file_path, filename=filename, user_id=current_user.id)
                    db.session.add(user_file)
                    db.session.commit()
                    flash('File LINK added')  # change!     
            else:
                os.system('mv ' + tmp_file_path + ' '+ file_path)
                user_file = File(filepath=file_path, filename=filename, user_id=current_user.id)
                db.session.add(user_file)
                db.session.commit()
                flash('File added')
            return redirect(url_for('upload'))
            # return send_file(file_path, as_attachment=True, attachment_filename='testfile')  # download file
    return render_template('upload.html')

@app.route('/files', methods=['GET', 'POST'])
@login_required
def user_files():
    files = File.query.filter_by(user_id=current_user.id)
    return render_template('files.html', files=files)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('user_files'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('user_files')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/admin', methods=['GET', 'POST'])
@login_required
def admin():
    if current_user.is_admin:
        form = AddUserForm()
        if form.validate_on_submit():
            user = User(username=form.username.data, is_admin=form.is_admin.data)
            user.set_password(form.password.data)
            db.session.add(user)
            db.session.commit()
            flash('User added')
    else:
        return redirect(url_for('user_files'))
    return render_template('admin.html', title='Admin', form=form)