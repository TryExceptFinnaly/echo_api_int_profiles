import os

from fastapi import FastAPI, File, Request
from datetime import datetime
from fastapi.responses import FileResponse, HTMLResponse, RedirectResponse
import starlette.status as status

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
    print_requests_to_file(f'{request.headers}\n\nBody Data:\n{request_body}', 'REMD')
    return {"message": "EMDR request received"}


@app.get("/wsdl/EMDR")
def emdr_get():
    return FileResponse(path='wsdl/EMDR.xml', media_type='application/xml')


@app.post("/odii", status_code=201)
async def odii(request: Request):
    request_body = await request.json()
    # request_body = request_body.decode('utf-8')
    print_requests_to_file(f'{request.headers}\n\nBody Data:\n{request_body}', 'ODII')
    return {"message": "ODII request received"}


@app.post("/conclusion/full", status_code=201)
async def eris(request: Request):
    request_body = await request.json()
    # request_body = request_body.decode('utf-8')
    print_requests_to_file(f'{request.headers}\n\nBody Data:\n{request_body}', 'ERIS')
    return {"message": "ERIS request received"}


@app.get("/favicon.ico")
def favicon():
    return File('static/favicon.ico', media_type='image/vnd.microsoft.icon')


@app.get("/logs")
def list_logs():
    list_logs = []
    content = f""""""
    with os.scandir(REQUESTS_FOLDER) as scandir:
        for entry in scandir:
            if entry.is_file(follow_symlinks=False):
                list_logs.append(entry.name)
                content = f"""<form action="/logs/{entry.name}">
                            <input type="submit" formmethod="get" value="{entry.name}">
                            <input type="submit" formmethod="post" value="delete">
                            </form>""" + content
    css = 'input{' \
          'width: 250px' \
          '}' \
          'input[value="delete"]{' \
          'width: 50px' \
          '}'
    head = f"""<head><style type="text/css">{css}</style></head>"""
    content = f"""{head}<body>{content}</body>"""
    return HTMLResponse(content=content)


@app.get("/logs/{log_name}")
def open_log(log_name: str):
    return FileResponse(path=f'requests/{log_name}')


@app.post("/logs/{log_name}")
def delete_log(log_name: str):
    try:
        os.remove(path=f'requests/{log_name}')
        return RedirectResponse('/logs', status_code=status.HTTP_302_FOUND)
    except Exception as exc:
        return {"message": f"Log {log_name} deletion error: {exc}."}
