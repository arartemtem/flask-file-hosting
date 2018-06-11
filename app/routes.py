import os
from flask import Flask, render_template, request, flash, redirect, url_for, send_file
from app import app
from werkzeug.utils import secure_filename
from app import functions
# from app.forms import LoginForm, UploadForm

@app.route('/upload', methods=['GET', 'POST'])
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
            os.system('mv ' + tmp_file_path + ' '+ file_path)
            return redirect('/upload')
            # return send_file(file_path, as_attachment=True, attachment_filename='testfile')  # download file
    return render_template('upload.html')

@app.route('/files', methods=['GET', 'POST'])
def user_files():
    files = [
        {
            'filename': 'test1.jpg'
        },
        {
            'filename': 'test2.pdf'
        }, 
        {
            'filename': 'test3.avi'
        }
    ]
    return render_template('files.html', files=files)
