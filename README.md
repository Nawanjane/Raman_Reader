---

# Raman ASC File Processor

A Flask-based web application for uploading, processing, and visualizing `.asc` files. Users can register, log in, upload files, view charts for processed data, and process entire folders. The application uses Flask, SQLAlchemy, Flask-Login, and Bootstrap for the user interface.

---

## Features

- **User Authentication**: Register, log in, and manage sessions.
- **File Upload**: Upload multiple `.asc` files.
- **Data Visualization**: Generate charts from `.asc` file content.
- **Folder Processing**: Process entire directories for `.asc` files.
- **Responsive UI**: Built with Bootstrap for a modern and user-friendly design.

---

## Setup Instructions

### Prerequisites

Ensure you have the following installed:

- Python (>= 3.8)
- pip (Python package manager)
- Git (optional, for cloning the repository)

---

### Installation

1. **Clone the Repository** (or download as ZIP and extract):
   ```bash
   git clone https://github.com/Nawanjane/Raman_Reader.git
   cd Raman_Reader
   ```

2. **Set Up a Virtual Environment** (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate       # On Linux/macOS
   venv\Scripts\activate          # On Windows
   ```

3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Environment Variables**:

Set the following environment variables for secure configuration:

- `FLASK_APP=app.py`
- `FLASK_ENV=development`
- `SECRET_KEY`: Your application's secret key.

For Linux/macOS:
```bash
export FLASK_APP=app.py
export FLASK_ENV=development
export SECRET_KEY="your-secret-key"
```

For Windows (Command Prompt):
```bash
set FLASK_APP=app.py
set FLASK_ENV=development
set SECRET_KEY="your-secret-key"
```


5. **Set Up the Database**:
   Initialize the SQLite database.
   ```bash
   flask shell
   from app import db
   db.create_all()
   exit()
   ```

6. **Run the Application**:
   ```bash
   flask run
   ```

7. Open your browser and navigate to:
   ```
   http://127.0.0.1:5000
   ```

---

### File Structure

```plaintext
flask-asc-processor/
├── app.py                 # Main application file
├── models.py              # Database models
├── scripts/
│   └── process_file.py    # Custom file processing logic
├── templates/             # HTML templates
│   ├── base.html
│   ├── login.html
│   ├── register.html
│   ├── index.html
│   ├── chart.html
│   └── process_folder.html
├── static/                # Static files (CSS, JS, images)
├── uploads/               # Uploaded `.asc` files
├── requirements.txt       # Python dependencies
└── README.md              # Project documentation
```

---



### Usage

1. **Register and Log In**:
   - Register as a new user on the `/register` page.
   - Log in to access the application features.

2. **Upload Files**:
   - Upload `.asc` files on the home page.
   - View a list of uploaded files.

3. **View Charts**:
   - Click "View Chart" for a file to visualize its content.

4. **Process Folders**:
   - Use the "Process Folder" feature to process all `.asc` files in a directory.

---

### Customization

1. **UI Customization**:
   - Modify the Bootstrap-based templates in the `templates/` folder.

2. **File Processing**:
   - Update the logic in `scripts/process_file.py` to customize file handling.

3. **Database**:
   - Extend models in `models.py` for additional features.

---

### Troubleshooting

- **Dependencies Issue**:
  Ensure all required libraries are installed:
  ```bash
  pip install -r requirements.txt
  ```

- **Database Errors**:
  Delete `database.db` and reinitialize:
  ```bash
  rm database.db
  flask shell
  from app import db
  db.create_all()
  exit()
  ```

- **File Upload Errors**:
  Check permissions for the `uploads/` directory.

---

### Contributing

Contributions are welcome! Follow these steps:

1. Fork the repository.
2. Create a new branch: `git checkout -b feature-name`.
3. Commit changes: `git commit -m "Add feature name"`.
4. Push to the branch: `git push origin feature-name`.
5. Submit a pull request.

---

### License

This project is licensed under the MIT License. See the `LICENSE` file for details.

---

### Contact

For questions or support, please reach out to:

- **Email**: nimendradandeniya.com
- **GitHub**: [Nawanjane](https://github.com/Nawanjane)

---
