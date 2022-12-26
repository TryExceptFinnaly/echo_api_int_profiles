import os
import json

from flask import Flask, send_from_directory, render_template, request
from flask_restful import Api

app = Flask(__name__)
app.logger.setLevel('INFO')
api = Api(app)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/odii/', methods=('GET', 'POST'))
def odii():
    if request.method == 'POST':
        app.logger.info(f'Headers:\n{request.headers}')
        app.logger.info(f'Body Data:\n{json.loads(request.data)}')
        return '', 201
    else:
        return render_template('index.html')


@app.route('/conclusion/full', methods=('GET', 'POST'))
def eris():
    if request.method == 'POST':
        app.logger.info(f'Headers:\n{request.headers}')
        app.logger.info(f'Body Data:\n{json.loads(request.data)}')
        return '', 201
    else:
        return render_template('index.html')


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico',
                               mimetype='image/vnd.microsoft.icon')


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=80)
    # ssl_context=('certificate/cert.pem', 'certificate/key.pem'))
