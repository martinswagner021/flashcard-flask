from flask import Blueprint, request, redirect, flash, url_for
from .middleware.verify_csv_pattern import verify_csv_pattern
from db.operations import create_deck

upload_bp = Blueprint('upload', __name__)

@upload_bp.route('/', methods=['GET','POST'])
def upload():
    if request.method == 'GET':
        return '''
        <h1>Upload CSV File</h1>
        <form method="POST" enctype="multipart/form-data">
            <input type="file" name="file" accept=".csv">
            <input type="text" name="table_name" placeholder="Table Name">
            <input type="submit" value="Upload">
        </form>
        '''
    if request.method == 'POST':
        file = request.files.get("file")

        verify_csv_pattern(file, request)

        table_name = request.form.get("table_name")
        if not table_name:
            flash("Please provide a table name.")
            return redirect(request.url)
        
        try:
            create_deck(file, table_name)
            flash(f"File uploaded successfully!") 
            return redirect(url_for('index'))
        except:
            flash(f"An error occurred while uploading the file.")
