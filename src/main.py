import io
import asyncio

from fastapi import FastAPI, Request, File, Query
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

import whisper
import cv2
import os
import glob
from docx import Document
from docx.shared import Inches

app = FastAPI()

app.mount('/static', StaticFiles(directory='static'), name='static')
template = Jinja2Templates(directory='templates')

@app.get('/', response_class=HTMLResponse)
def index(request: Request):
    return template.TemplateResponse('index.html',  {"request": request, "result": None})

@app.post('/')
def add_audio(request: Request, file: bytes = File()):
    with open('audio.mp4', 'wb') as f:
        f.write(file)
    
    path = "static"
    files = glob.glob(os.path.join(path, "*.jpg" and "*.docx"))
    for file in files:
        os.remove(file)

    data = request.form()
    model_type = asyncio.run(data)['model_type']
    model = whisper.load_model(model_type)
    result = model.transcribe(audio="audio.mp4", fp16=False)
    segments = result['segments']

    seconds = []
    for item in range(len(segments)):
        seconds.append(segments[item]['start'])

    lines = []
    for item in range(len(segments)):
        lines.append(segments[item]['text'])
    

    vidcap = cv2.VideoCapture("audio.mp4")
    success,image = vidcap.read()
    success = True
    while success:
        for sec in seconds: 
            vidcap.set(cv2.CAP_PROP_POS_MSEC,(sec*1000))
            success,image = vidcap.read()
            cv2.imwrite("static/" + str(sec) + ".jpg", image)  
        break
    else:
        print("Error Saving Images")

    document = Document()

    document.add_heading('Whisper Generated Guide', 0)

    for second, line in zip(seconds, lines):
        document.add_picture("static/" + str(second) + ".jpg", width=Inches(1.25))
        document.add_paragraph(line)

    document.save('static/output.docx')

    return template.TemplateResponse('index.html',  {"request": request, "result": "Download Guide"})