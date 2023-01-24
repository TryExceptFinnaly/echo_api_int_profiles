from fastapi import FastAPI, File, Request

from datetime import datetime
from fastapi.responses import JSONResponse, FileResponse

app = FastAPI()
REQUESTS_FOLDER = 'requests'


def print_requests_to_file(text, profile):
    filename = f"{REQUESTS_FOLDER}/{profile}_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.txt"
    print(text, file=open(filename, "w", encoding='utf-8'))


@app.get("/")
def index():
    return JSONResponse(content={"message": "Welcome to my API"}, status_code=200)


@app.post("/wsdl/EMDR")
def emdr_post(request: Request):
    print_requests_to_file(f'Headers:\n{request.headers}\nBody Data:\n{request.json()}', 'REMD')
    return JSONResponse(content={"message": "EMDR request received"}, status_code=201)


@app.get("/wsdl/EMDR")
def emdr_get():
    return FileResponse(path='wsdl/EMDR.xml', media_type='application/xml')


@app.post("/odii")
def odii(request: Request):
    print_requests_to_file(f'Headers:\n{request.headers}\nBody Data:\n{request.json()}', 'ODII')
    return JSONResponse(content={"message": "ODII request received"}, status_code=201)


@app.post("/conclusion/full")
def eris(request: Request):
    print_requests_to_file(f'Headers:\n{request.headers}\nBody Data:\n{request.json()}', 'ERIS')
    return JSONResponse(content={"message": "ERIS request received"}, status_code=201)


@app.get("/favicon.ico")
def favicon():
    return File('static/favicon.ico', media_type='image/vnd.microsoft.icon')
