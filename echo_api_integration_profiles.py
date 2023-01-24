import os

from fastapi import FastAPI, File, Request
from datetime import datetime
from fastapi.responses import FileResponse

app = FastAPI(
    title='Echo API server for integration profiles'
)
REQUESTS_FOLDER = 'requests'


def print_requests_to_file(text, profile):
    filename = f"{REQUESTS_FOLDER}/{profile}_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.txt"
    print(text, file=open(filename, "w", encoding='utf-8'))


@app.get("/")
def main():
    return {"message": "Welcome to my API server"}


@app.post("/wsdl/EMDR", status_code=201)
async def emdr_post(request: Request):
    request_body = await request.body()
    request_body = request_body.decode('utf-8')
    print_requests_to_file(f'{request.headers}\nBody Data:\n{request_body}', 'REMD')
    return {"message": "EMDR request received"}


@app.get("/wsdl/EMDR")
def emdr_get():
    return FileResponse(path='wsdl/EMDR.xml', media_type='application/xml')


@app.post("/odii", status_code=201)
async def odii(request: Request):
    request_body = await request.body()
    request_body = request_body.decode('utf-8')
    print_requests_to_file(f'{request.headers}\nBody Data:\n{request_body}', 'ODII')
    return {"message": "ODII request received"}


@app.post("/conclusion/full", status_code=201)
async def eris(request: Request):
    request_body = await request.body()
    request_body = request_body.decode('utf-8')
    print_requests_to_file(f'{request.headers}\nBody Data:\n{request_body}', 'ERIS')
    return {"message": "ERIS request received"}


@app.get("/favicon.ico")
def favicon():
    return File('static/favicon.ico', media_type='image/vnd.microsoft.icon')


@app.get("/logs/")
def list_logs():
    list_logs = []
    with os.scandir(REQUESTS_FOLDER) as scandir:
        for entry in scandir:
            if entry.is_file(follow_symlinks=False):
                list_logs.append(entry.name)
    return list_logs


@app.get("/logs/{log_name}")
def open_log(log_name: str):
    return FileResponse(path=f'requests/{log_name}', media_type='text')
