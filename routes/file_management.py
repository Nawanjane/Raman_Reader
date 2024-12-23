from flask import Blueprint, request, redirect, url_for, render_template, session, flash
import os
from scripts.process_file import read_asc_file
from app import db
from models.file import File

file_management_blueprint = Blueprint('file_management', __name__)
UPLOAD_FOLDER = 'uploads'

@file_management_blueprint.route('/upload', methods=['GET', 'POST'])
def upload():
    if 'user_id' not in session:
        flash("Please log in to upload files.", "error")
        return redirect(url_for('auth.login'))

    user_id = session['user_id']
    user_folder = os.path.join(UPLOAD_FOLDER, str(user_id))
    os.makedirs(user_folder, exist_ok=True)

    if request.method == 'POST':
        files = request.files.getlist('file')
        for file in files:
            if file and file.filename.endswith('.asc'):
                filepath = os.path.join(user_folder, file.filename)
                file.save(filepath)

                # Save file metadata in the database
                new_file = File(filename=file.filename, filepath=filepath, user_id=user_id)
                db.session.add(new_file)
                db.session.commit()

        flash("Files uploaded successfully!", "success")
        return redirect(url_for('file_management.view_files'))

    return render_template('upload.html')

@file_management_blueprint.route('/files', methods=['GET'])
def view_files():
    if 'user_id' not in session:
        flash("Please log in to view your files.", "error")
        return redirect(url_for('auth.login'))

    user_id = session['user_id']
    user_files = File.query.filter_by(user_id=user_id).all()
    return render_template('files.html', files=user_files)
