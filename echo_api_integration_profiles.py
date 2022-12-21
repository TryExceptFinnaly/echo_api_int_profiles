import os

from flask import Flask, send_from_directory, render_template, request
from flask_restful import Api

app = Flask(__name__)
api = Api(app)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/odii/', methods=('GET', 'POST'))
def odii():
    if request.method == 'POST':
        print(request)
        print(request.headers)
        print(request.data.decode(encoding='UTF-8'))
        return '', 201
    else:
        return render_template('index.html')


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico',
                               mimetype='image/vnd.microsoft.icon')


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
    # ssl_context=('certificate/cert.pem', 'certificate/key.pem'))
