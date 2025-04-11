from flask import flash, redirect

def verify_csv_pattern(file, request):
    """
    Middleware to verify the uploaded CSV file.
    """
    if not file or not file.filename.endswith(".csv"):
        flash("Please provide a CSV file and a table name.")
        return redirect(request.url)
        
    header = file.readline().decode('utf-8').strip().split(',')

    if header != ['Front', 'Back', 'Plus']:
        flash("Invalid CSV format. Expected headers: Front, Back, Part of speech.")
        return redirect(request.url)