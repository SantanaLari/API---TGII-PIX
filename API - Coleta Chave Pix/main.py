from trata_comentario import TrataComentario
from typing import Union
from fastapi import FastAPI
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from starlette.requests import Request
from starlette.templating import Jinja2Templates
import json

app = FastAPI()

templates = Jinja2Templates(directory="templates")
uploaded_file_data = None

@app.get("/")
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/upload_arquivo/")
async def upload_arquivo(request: Request, file: UploadFile = File(...)):
    global uploaded_file_data
    if not file.filename.endswith(".json"):
        raise HTTPException(status_code=400, detail="Only JSON files are allowed.")
    
    try:
        contents = await file.read()
        uploaded_file_data = json.loads(contents)
        return JSONResponse(status_code=200, content={"message": "File uploaded successfully."})
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred while processing the file: {str(e)}")

@app.get("/exibe_contagem/{chave_json}")
async def contagem_pix(chave_json:str):
    global uploaded_file_data

    if uploaded_file_data:
        pix = TrataComentario(uploaded_file_data, chave_json)
        lista_comentarios_coletados = pix.coleta_comentario()
        chaves_analisadas = pix.filtra_comentario(lista_comentarios_coletados)
        contagem = pix.contabiliza_chave(chaves_analisadas)

        return contagem
    else:
        return JSONResponse(status_code=404, content={"message":"No file uploaded yet."})

if __name__ == '__main__':
    index()
