import os
import re
import flask
from flask import Flask, request, redirect, url_for, send_from_directory, Response
from flask_cors import CORS
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = 'static/uploads/'

app = Flask(__name__)
CORS(app)
app.secret_key = "secret key"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/upload', methods=['POST'])
def upload_video():
    response = flask.Response()
    file = request.files['file']
    filename = secure_filename(file.filename)
    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    print(filename)
    return flask.Response(filename, 200)


@app.route('/handle/<string:filename>', methods=['GET'])
def handle_video(filename):
    video = open(os.path.join(app.config['UPLOAD_FOLDER'], filename), 'rb')
    #TODO:video handler
    return 'Handled'

@app.route('/download/<string:filename>')
def download_video(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


@app.route('/display/<string:filename>')
def display_video(filename):
    # print('display_video filename: ' + filename)
    return redirect(url_for('static', filename='uploads/' + filename), code=301)


def get_chunk(file_path, byte1=None, byte2=None):
    file_size = os.stat(file_path).st_size
    start = 0

    if byte1 < file_size:
        start = byte1
    if byte2:
        length = byte2 + 1 - byte1
    else:
        length = file_size - start

    with open(file_path, 'rb') as f:
        f.seek(start)
        chunk = f.read(length)
    return chunk, start, length, file_size


@app.route('/video_stream/<string:filename>')
def get_file(filename):
    range_header = request.headers.get('Range', None)
    byte1, byte2 = 0, None
    if range_header:
        match = re.search(r'(\d+)-(\d*)', range_header)
        groups = match.groups()

        if groups[0]:
            byte1 = int(groups[0])
        if groups[1]:
            byte2 = int(groups[1])

    chunk, start, length, file_size = get_chunk(os.path.join(UPLOAD_FOLDER, filename), byte1, byte2)
    response = Response(chunk, 206, mimetype='video/mp4',
                    content_type='video/mp4', direct_passthrough=True)
    response.headers.add('Content-Range', 'bytes {0}-{1}/{2}'.format(start, start + length - 1, file_size))
    response.headers.add('Accept-Ranges', 'bytes')
    return response


if __name__ == "__main__":
    app.run(host='localhost', port=3000)