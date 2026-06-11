# main.py
from fastapi import FastAPI, Request, Form, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from app.models import Tarea, MatrizEisenhower
import uuid
import os
import requests

app = FastAPI(
    title="EisenFlow API Core",
    description="API para clasificar tareas según la Matriz de Eisenhower y gestionar un tablero Kanban.",
    version="1.0.0")

# Montar archivos estáticos
os.makedirs("app/static", exist_ok=True)
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Configurar motor de plantillas
templates = Jinja2Templates(directory="app/templates")

matriz = MatrizEisenhower() # Instanciamos el backend en memoria

@app.get("/", response_class=HTMLResponse)
async def dashboard(request: Request):
    """Renderiza el dashboard Kanban de EisenFlow."""
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={"tablero": matriz.tablero_kanban}
    )

@app.get("/api/health")
async def health_check():
    """Endpoint de salud del sistema."""
    return {"message": "EisenFlow API is running. Go to /docs or /redoc for documentation."}

@app.post("/crear-tarea", response_class=RedirectResponse)
async def crear_tarea_formulario(
    titulo: str = Form(...),
    urgente: bool = Form(default=False),
    importante: bool = Form(default=False)
):
    """Procesa el formulario HTML para crear y clasificar una tarea, y redirige al dashboard."""
    nueva_tarea = Tarea(
        titulo=titulo,
        urgente=urgente,
        importante=importante
    )
    matriz.clasificar_tarea(nueva_tarea)
    return RedirectResponse(url="/", status_code=303)

@app.post("/tarea/clasificar", response_model=Tarea)
async def crear_y_clasificar_tarea(tarea: Tarea):
     # Pasamos el JSON recibido por la infraestructura de la clase POO
     tarea_procesada = matriz.clasificar_tarea(tarea)
     return tarea_procesada

@app.get("/tablero")
async def obtener_tablero():
    return matriz.tablero_kanban