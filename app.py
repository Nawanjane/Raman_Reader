from flask import Flask
from routes.auth import auth_blueprint
from routes.file_management import file_management_blueprint
from routes.home import home_blueprint
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///instance/users.db'
app.config['UPLOAD_FOLDER'] = 'uploads'

os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs('instance', exist_ok=True)

db = SQLAlchemy(app)

# Register Blueprints
app.register_blueprint(auth_blueprint, url_prefix="/auth")
app.register_blueprint(file_management_blueprint, url_prefix="/files")
app.register_blueprint(home_blueprint)

if __name__ == '__main__':
    app.run(debug=True)
