import os
import base64

from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/upload/', methods=['POST'])
def file_upload():
    # convert request body to valid base64 string
    encoded_image = request\
        .data\
        .decode()\
        .replace('data:image/png;base64,', '')\
        .replace(' ', '+')

    # decode image content
    content = base64.b64decode(encoded_image)

    # TODO: recognize digit send response back
    with open('test.png', 'wb') as f:
        f.write(content)

    return 'ok'

if __name__ == '__main__':
    app.run(debug=True)
