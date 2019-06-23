import os
from datetime import datetime
import time

import hashlib
from flask_login import current_user
from flask import flash, redirect, url_for, send_file
from sqlalchemy import desc

from app import app, db
from app.models import File, FilePath


class FileActions:

    def delete_file(self, file):
        file_name = file.filename
        file_path = FilePath.query.filter_by(id=file.filepath_id).first()
        db.session.delete(file)
        db.session.commit()
        file_path_file = File.query.filter_by(filepath_id=file_path.id).first()
        if not file_path_file:
            os.remove(file_path.filepath)
            os.removedirs(file_path.filepath[:-26])
            db.session.delete(file_path)
            db.session.commit()
        flash('File "' + file_name + '" is deleted', 'info')
        return redirect(url_for('user_files'))

    def download_file(self, file_id):
        file = File.query.filter_by(id=file_id).first()
        file_path = FilePath.query.filter_by(id=file.filepath_id).first()
        file_name = file.filename
        if current_user.is_anonymous and not file.is_shared:
            flash('Access Denied!', 'danger')
            return redirect(url_for('login'))
        elif (current_user.is_anonymous and file.is_shared) or current_user.id == file.user_id or file.is_shared:
            return send_file(file_path, as_attachment=True, attachment_filename=file_name)
        else:
            return redirect(url_for('user_files'))

    def file_list(self, form):
        if form.validate_on_submit() and form.file_name.data != '':
            files = File.query.filter(File.user_id == current_user.id,
                                      File.filename.like(f'%{form.file_name.data}%'))
        else:
            files = File.query.filter_by(user_id=current_user.id).order_by(desc(File.uploadtime))
        return files

    def sharing(self, user_id, file_id, share: bool):
        file = File.query.filter_by(id=file_id).first()
        if user_id == file.user_id:
            file.is_shared = True if share else False
            return db.session.commit()
        else:
            return flash('Error', 'danger')

    def upload_file(self, request):
        if request.method == 'POST':
            file, temp_file_path = self._check_file(request)
            if file:
                file_exists, file_path = self._check_file_exists(file)
                if file_exists:
                    os.remove(temp_file_path)
                    filepath_id = FilePath.query.filter_by(filepath=file_path).first().id
                    is_user_file = File.query.filter_by(filepath_id=filepath_id, user_id=current_user.id).first()
                    if is_user_file:
                        exists_name = is_user_file.filename
                        flash('File already exists with name "' + exists_name + '"', 'warning')
                    else:
                        user_file = File(filepath_id=filepath_id, filename=file.filename, uploadtime=datetime.utcnow(),
                                         is_shared=False, user_id=current_user.id)
                        db.session.add(user_file)
                        db.session.commit()
                        flash('File LINK added', 'success')
                else:
                    os.rename(temp_file_path, file_path)
                    filepath = FilePath(filepath=file_path)
                    db.session.add(filepath)
                    filepath = FilePath.query.filter_by(filepath=file_path).first()
                    user_file = File(filepath_id=filepath.id, filename=file.filename, uploadtime=datetime.utcnow(),
                                     is_shared=False,
                                     user_id=current_user.id)
                    db.session.add(user_file)
                    db.session.commit()
                    flash('File added', 'success')
                return redirect(request.url)

    def _check_file(self, request):
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part', 'warning')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file', 'warning')
            return redirect(request.url)
        temp_file_path = os.path.join(app.config['UPLOAD_FOLDER'], str(time.time()).replace('.', '-'))
        file.save(temp_file_path)
        return file, temp_file_path

    def _check_file_exists(self, file):
        md5_filename = hashlib.md5(file.read()).hexdigest()
        dir_for_file = os.path.join(app.config['UPLOAD_FOLDER'], md5_filename[0:3], md5_filename[3:6])
        if not os.path.exists(dir_for_file):
            os.makedirs(dir_for_file)
        new_filename = md5_filename[7:]
        file_path = os.path.join(dir_for_file, new_filename)
        return os.path.exists(file_path), file_path
