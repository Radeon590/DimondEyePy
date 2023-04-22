import os
import flask
from flask import Flask, request, redirect, url_for, send_from_directory, make_response, jsonify
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


if __name__ == "__main__":
    app.run(host='localhost', port=3000)