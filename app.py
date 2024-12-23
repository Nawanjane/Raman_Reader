# app.py
from flask import Flask, render_template, request, redirect, url_for, send_from_directory
import os
from scripts.process_file import read_asc_file

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/', methods=['GET', 'POST'])
def index():
    

    if request.method == 'POST':
        files = request.files.getlist('file')
        stack = 'stack' in request.form  # Check if the stack checkbox is checked
        filenames = []
        for file in files:
            if file and '.' in file.filename and file.filename.rsplit('.', 1)[1].lower() == 'asc':
                filename = file.filename
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(file_path)
                filenames.append(filename)
        return redirect(url_for('chart', filenames=','.join(filenames), stack=stack))
    return render_template('index.html')


@app.route('/chart/<filenames>')
def chart(filenames):
    stack = request.args.get('stack') == 'True'
    filenames = filenames.split(',')
    datasets = []
    all_intensities = []  # List to hold all intensity lists

    # Read and store intensities from all files
    for filename in filenames:
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        shifts, intensities = read_asc_file(file_path)
        all_intensities.append(intensities)

    if stack:
        # Calculate the average intensity for each shift
        # This assumes all files have the same number of data points and corresponding shifts
        averaged_intensities = [sum(x) / len(x) for x in zip(*all_intensities)]
        datasets = [{'shifts': shifts, 'intensities': averaged_intensities, 'label': 'Averaged Data'}]
    else:
        for filename, intensities in zip(filenames, all_intensities):
            if len(intensities) > 0:  # Check if intensities list has elements
                shifts, intensities = read_asc_file(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                datasets.append({'shifts': shifts, 'intensities': intensities, 'label': filename})


    return render_template('chart.html', datasets=datasets)

@app.route('/process-folder', methods=['GET', 'POST'])
def process_folder():
    if request.method == 'POST':
        # In this example, the user provides the folder path via a form input
        folder_path = request.form.get('folder_path')
        new_folder_path = os.path.join(folder_path, 'processed')

        # Create a new directory for the processed results
        os.makedirs(new_folder_path, exist_ok=True)

        # Process each subfolder
        for subfolder_name in os.listdir(folder_path):
            subfolder_path = os.path.join(folder_path, subfolder_name)
            if os.path.isdir(subfolder_path):
                # Stack the data from .asc files in the subfolder
                stacked_data, chart_image = stack_data_from_subfolder(subfolder_path)

                # Save the stacked data as a new .asc file
                stacked_filename = f'{subfolder_name}_stacked.asc'
                save_stacked_data(stacked_data, os.path.join(new_folder_path, stacked_filename))

                # Save the chart image
                chart_image_filename = f'{subfolder_name}_chart.png'
                chart_image.save(os.path.join(new_folder_path, chart_image_filename))

        return redirect(url_for('folder_processed_successfully'))
    return render_template('process_folder.html')


if __name__ == '__main__':
    app.run(debug=True)