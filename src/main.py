import convertguideapp
import os.path

from fastapi import FastAPI, Request, File, Form
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

app = FastAPI()

app.mount('/static', StaticFiles(directory='static'), name='static')
app.mount('/static/temp', StaticFiles(directory='static/temp'), name='temp')
template = Jinja2Templates(directory='templates')

@app.get('/', response_class=HTMLResponse)
def index(request: Request):
    templateResponse = template.TemplateResponse('index.html',  {"request": request, "disabled": True, "result": False})
    print(templateResponse)
    return templateResponse

@app.post('/guide/')
def audio(request: Request, file: bytes = File(), model_type: str = Form(), screenshots: int = Form()):
    dir = "static/temp/"
    doc = 'output.docx'
    video = "audio.mp4"
    completeName = os.path.join(dir, video) 
    convertguideapp.clean_path(dir)
    with open(completeName, 'wb') as f:
        f.write(file)
    convertguideapp.convert_guide(model_type, screenshots, dir, completeName, doc)
    templateResponse = template.TemplateResponse('index.html',  {"request": request, "disabled": False, "result": True})
    print(templateResponse)
    return templateResponse
    