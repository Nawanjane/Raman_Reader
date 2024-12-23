from flask import Flask, render_template, redirect, url_for, request, flash, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from models import db, User, File
from forms import RegistrationForm, LoginForm, FileUploadForm
import os
from flask.cli import with_appcontext
import click
from werkzeug.security import generate_password_hash


# Initialize the Flask application
app = Flask(__name__)
app.config.from_object('config.Config')



# Initialize database and login manager
db.init_app(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'


@app.cli.command('init-db')
@with_appcontext
def init_db():
    db.create_all()
    print("Database initialized.")

# Create a user loader function for flask-login
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))



@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data, method='pbkdf2:sha256')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Account created!', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and check_password_hash(user.password, form.password.data):
            login_user(user)
            flash('Login successful!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Login failed. Check your email and password.', 'danger')
    return render_template('login.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out!', 'info')
    return redirect(url_for('login'))

@app.route('/index')
@login_required
def index():
    form = FileUploadForm()
    files = File.query.filter_by(user_id=current_user.id).all()
    if form.validate_on_submit():
        file = form.file.data
        filename = file.filename
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        new_file = File(filename=filename, filepath=filepath, user_id=current_user.id)
        db.session.add(new_file)
        db.session.commit()
        flash('File uploaded successfully!', 'success')
        return redirect(url_for('index'))
    return render_template('index.html', form=form, files=files)

@app.route('/chart/<int:file_id>')
@login_required
def chart(file_id):
    file = File.query.get_or_404(file_id)
    if file.user_id != current_user.id:
        flash('You cannot access this file.', 'danger')
        return redirect(url_for('index'))
    
    # Render your chart (Assume you have chart logic here)
    return render_template('chart.html', file=file)

if __name__ == '__main__':
    app.run(debug=True)

