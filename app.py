from flask import Flask, render_template, request, redirect, url_for, flash, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from models import db, bcrypt, User, File
from scripts.process_file import read_asc_file
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hZdXEt5QyOZIZG4l3fOy2vmIreKoKgk4'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['UPLOAD_FOLDER'] = 'uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

db.init_app(app)
bcrypt.init_app(app)

login_manager = LoginManager(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Enhanced error handler
@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html', error=error), 404

@app.errorhandler(500)
def internal_error(error):
    return render_template('500.html', error=error), 500

# User registration with better error messages
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        if not username or not password:
            flash('Username and Password are required.', 'error')
            return redirect(url_for('register'))
        if password != confirm_password:
            flash('Passwords do not match. Please try again.', 'error')
            return redirect(url_for('register'))
        if User.query.filter_by(username=username).first():
            flash('Username already exists. Please choose a different one.', 'error')
            return redirect(url_for('register'))

        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        user = User(username=username, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Account created successfully! You can now log in.', 'success')
        return redirect(url_for('login'))

    return render_template('register.html')

# User login with better feedback
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if not username or not password:
            flash('Please fill in both fields.', 'error')
            return redirect(url_for('login'))

        user = User.query.filter_by(username=username).first()
        if user and bcrypt.check_password_hash(user.password, password):
            login_user(user)
            flash('Login successful!', 'success')
            return redirect(url_for('index'))

        flash('Invalid username or password. Please try again.', 'error')
    return render_template('login.html')

# File upload with enhanced error checking
@app.route('/', methods=['GET', 'POST'])
@login_required
def index():
    if request.method == 'POST':
        files = request.files.getlist('file')

        if not files:
            flash('No files selected. Please upload a file.', 'error')
            return redirect(url_for('index'))

        for file in files:
            if file and '.' in file.filename and file.filename.rsplit('.', 1)[1].lower() == 'asc':
                filename = file.filename
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                try:
                    file.save(file_path)
                    new_file = File(filename=filename, owner=current_user)
                    db.session.add(new_file)
                except Exception as e:
                    flash(f'Error saving file {filename}: {str(e)}', 'error')
            else:
                flash(f'Invalid file type for {file.filename}. Only .asc files are allowed.', 'error')
        db.session.commit()
        flash('Files uploaded successfully!', 'success')

    user_files = File.query.filter_by(user_id=current_user.id).all()
    return render_template('index.html', files=user_files)

@app.route('/chart/<int:file_id>')
@login_required
def chart(file_id):
    file = File.query.filter_by(id=file_id, user_id=current_user.id).first_or_404()
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    try:
        shifts, intensities = read_asc_file(file_path)
        datasets = [{'shifts': shifts, 'intensities': intensities, 'label': file.filename}]
        return render_template('chart.html', datasets=datasets)
    except Exception as e:
        flash(f'Error processing file: {str(e)}', 'error')
        return redirect(url_for('index'))

@app.route('/process-folder', methods=['GET', 'POST'])
@login_required
def process_folder():
    if request.method == 'POST':
        folder_path = request.form['folder_path']
        if not folder_path:
            flash('Please specify a folder path.', 'error')
            return redirect(url_for('process_folder'))

        new_folder_path = os.path.join(folder_path, 'processed')
        try:
            os.makedirs(new_folder_path, exist_ok=True)
            # Add your folder processing logic here
            flash('Folder processed successfully!', 'success')
        except Exception as e:
            flash(f'Error processing folder: {str(e)}', 'error')

    return render_template('process_folder.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out successfully.', 'success')
    return redirect(url_for('login'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)

