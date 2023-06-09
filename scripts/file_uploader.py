# scripts/file_uploader.py
from werkzeug.utils import secure_filename
import os

def upload_files(request, upload_folder):
    if 'files' not in request.files:
        return 'No files part in the request.', 400

    files = request.files.getlist('files')

    if not files or files[0].filename == '':
        return 'No selected files.', 400

    for file in files:
        filename = secure_filename(file.filename)
        file.save(os.path.join(upload_folder, filename))

    return 'Files uploaded successfully.'
