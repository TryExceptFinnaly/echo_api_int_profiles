import os
import json

from flask import Flask, send_from_directory, render_template, request
from flask_restful import Api
from datetime import datetime

app = Flask(__name__)
app.logger.setLevel('INFO')
api = Api(app)

REQUESTS_FOLDER = 'requests'


def print_requests_to_file(text, profile):
    filename = f"{REQUESTS_FOLDER}/{profile}_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.txt"
    print(text, file=open(filename, "w"))


# logging.basicConfig(format='%(levelname)s:%(message)s', filename='api.log', level=logging.DEBUG, encoding='utf-8')

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/wsdl/EMDR')
def emdr():
    return send_from_directory(os.path.join(app.root_path, 'wsdl'), 'EMDR.xml')


@app.route('/odii/', methods=('GET', 'POST'))
def odii():
    if request.method == 'POST':
        print_requests_to_file(f'Headers:\n{request.headers}\nBody Data:\n{json.loads(request.data)}', 'ODII')
        return '', 201
    else:
        return render_template('index.html')


@app.route('/conclusion/full', methods=('GET', 'POST'))
def eris():
    if request.method == 'POST':
        print_requests_to_file(f'Headers:\n{request.headers}\nBody Data:\n{json.loads(request.data)}', 'ERIS')
        return '', 201
    else:
        return render_template('index.html')


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico',
                               mimetype='image/vnd.microsoft.icon')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
    # ssl_context=('certificate/cert.pem', 'certificate/key.pem'))
