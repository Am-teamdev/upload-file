import socket
from flask import Flask, render_template, request, redirect, url_for
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 1024 * 1024 * 1024

def path_to(filename : str):
    filename = secure_filename(filename)
    ext = os.path.splitext(filename)[1].lower()
    folder = ''
    if ext in ['.jpg', '.jpeg', '.png', '.gif']:
        folder = "images"
    elif ext in ['.pdf']:
        folder = "pdfs"
    elif ext in ['.zip', '.rar']:
        folder = "archives"
    else:
        folder = "other"

    path_save = os.path.join(app.config['UPLOAD_FOLDER'], folder)
    os.makedirs(path_save, exist_ok=True)
    return os.path.join(path_save, filename)

@app.route('/')
def upload_page():  # put application's code here
    return render_template('upload.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if request.method == 'POST':
        if 'files' not in request.files:
            return redirect(url_for('upload_page'))
        files = request.files.getlist('files')
        for file in files:
            if file.filename == '':
                return redirect(url_for('upload_page'))
            path = path_to(file.filename)
            file.save(path)
        return redirect(url_for('upload_page'))

if __name__ == '__main__':
    hostname = socket.gethostname()
    local_ip = socket.gethostbyname(hostname)

    port = 5000

    print(f"Server is running!")
    print(f"Access this site from other devices on the network at:")
    print(f"http://{hostname}:{port}")

    # اجرا کردن Flask روی همه IP ها
    app.run(host='0.0.0.0', port=port)
