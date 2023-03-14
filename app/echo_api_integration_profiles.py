import os
import starlette.status as status

from fastapi import FastAPI, File, Request
from datetime import datetime
from fastapi.responses import FileResponse, HTMLResponse, RedirectResponse, Response

app = FastAPI(
    title='Echo API server for integration profiles'
)
REQUESTS_FOLDER = 'requests'


def print_requests_to_file(text, profile):
    filename = f"{REQUESTS_FOLDER}/{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}_{profile}.txt"
    print(text, file=open(filename, "w", encoding='utf-8'))


@app.get("/")
def main():
    return {"message": "Welcome to my API server"}


@app.post("/wsdl/EMDR", status_code=500)
async def emdr_post(request: Request):
    request_body = await request.body()
    request_body = request_body.decode('utf-8')
    print_requests_to_file(f'{request.headers}\n\nBody Data:\n{request_body}', 'REMD')
    data = """<?xml version="1.0"?>
    <ns3:errors>
        <ns3:item>
                <ns3:code>INTERNAL_ERROR</ns3:code>
                <ns3:message>Внутренняя ошибка системы</ns3:message>
        </ns3:item>
    </ns3:errors>
    """
    return Response(content=data, media_type="application/xml")


@app.get("/wsdl/EMDR")
def emdr_get():
    return FileResponse(path='wsdl/EMDR.xml', media_type="application/xml")


@app.post("/odii", status_code=201)
async def odii(request: Request):
    request_body = await request.json()
    # request_body = request_body.decode('utf-8')
    print_requests_to_file(f'{request.headers}\n\nBody Data:\n{request_body}', 'ODII')
    return {"message": "ODII request received"}


@app.post("/conclusion/full", status_code=201)
async def eris(request: Request):
    request_body = await request.json()
    print_requests_to_file(f'{request.headers}\n\nBody Data:\n{request_body}', f'ERIS')
    return {"message": "ERIS request received"}


@app.post("/subscribe/", status_code=200)
async def subscribe(request: Request):
    request_body = await request.json()
    event = request_body['event']
    print_requests_to_file(f'{request.headers}\n\nBody Data:\n{request_body}', f'SUBSCRIBE_{event}')
    return {"message": "ODII request received"}


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
    list_logs.sort(reverse=True)

    head = f"""<head><link href="logs.css" rel="stylesheet"></head>"""
    for log in list_logs:
        content += f"""<form action="/logs/{log}">
        <input type="submit" formmethod="get" value="{log}">
        <input type="submit" formmethod="post" value="delete">
        </form>"""
    # alert = f"""
    # <div id="delete">
    # <div id="window">
    # <br>Всплывающее окошко!</br>
    # <a href="#" class="close">Закрыть окно</a>
    # </div>
    # </div>"""
    content = f"""{head}<body>{content}</body>"""
    return HTMLResponse(content=content)


@app.get("/logs.css")
def open_log():
    return FileResponse(path=f'styles/logs.css')


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
