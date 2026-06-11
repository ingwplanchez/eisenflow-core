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

@app.get("/tarea/{tarea_id}", response_model=Tarea)
async def obtener_detalle_tarea(tarea_id: str):
    """Obtiene los detalles de una tarea específica por su ID."""
    from fastapi import HTTPException
    tarea = matriz.obtener_tarea(tarea_id)
    if not tarea:
        raise HTTPException(status_code=404, detail="Tarea no encontrada")
    return tarea

@app.put("/tarea/{tarea_id}/mover", response_model=Tarea)
async def mover_tarea_estado(tarea_id: str, nuevo_estado: str):
    """Mueve una tarea a otra columna del tablero Kanban (To Do, In Progress, Done)."""
    from fastapi import HTTPException
    if nuevo_estado not in ["To Do", "In Progress", "Done"]:
        raise HTTPException(status_code=422, detail="Estado Kanban inválido. Debe ser: To Do, In Progress o Done")
    
    tarea = matriz.mover_tarea(tarea_id, nuevo_estado)
    if not tarea:
        raise HTTPException(status_code=404, detail="Tarea no encontrada")
    return tarea

@app.delete("/tarea/{tarea_id}")
async def eliminar_tarea_tablero(tarea_id: str):
    """Elimina una tarea por completo del tablero."""
    from fastapi import HTTPException
    exito = matriz.eliminar_tarea(tarea_id)
    if not exito:
        raise HTTPException(status_code=404, detail="Tarea no encontrada")
    return {"message": f"Tarea con ID {tarea_id} eliminada exitosamente"}