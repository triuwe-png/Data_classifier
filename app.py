from fastapi import FastAPI, Request, UploadFile, File
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import pandas as pd
import os
from model import clasificar_datos

app = FastAPI()
templates = Jinja2Templates(directory="templates")

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "resultado": None, "error": None})

@app.post("/clasificar", response_class=HTMLResponse)
async def clasificar(request: Request, archivo: UploadFile = File(...)):
    try:
        path = os.path.join(UPLOAD_FOLDER, archivo.filename)
        with open(path, "wb") as buffer:
            buffer.write(await archivo.read())

        df = pd.read_csv(path)
        resultado = clasificar_datos(df)
        tabla_html = resultado.to_html(classes="table table-striped", index=False)

        return templates.TemplateResponse("index.html", {"request": request, "resultado": tabla_html, "error": None})

    except Exception as e:
        return templates.TemplateResponse("index.html", {"request": request, "resultado": None, "error": str(e)})