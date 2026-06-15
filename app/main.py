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

def disparar_webhook_n8n(tarea: Tarea):
    """Envía la información de la tarea clasificada a n8n de forma tolerante a fallos."""
    env = os.getenv("N8N_ENV", "test").lower()
    
    if env == "production":
        url = "http://localhost:5678/webhook/eisenhower/tasks"
    else:
        url = "http://localhost:5678/webhook-test/eisenhower/tasks"
        
    payload = {
        "id": tarea.id,
        "titulo": tarea.titulo,
        "cuadrante": tarea.cuadrante.split(" ")[-1].replace("(", "").replace(")", "")  # Extrae "Q1", "Q2", etc.
    }
    
    try:
        # Petición no bloqueante con timeout corto por si el servidor n8n no está activo
        requests.post(url, json=payload, timeout=2.0)
    except Exception as e:
        # Silenciamos el error para no romper la experiencia de la API
        print(f"[Webhook n8n Warning] No se pudo enviar el webhook a n8n: {e}")

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
    tarea_procesada = matriz.clasificar_tarea(nueva_tarea)
    disparar_webhook_n8n(tarea_procesada)
    return RedirectResponse(url="/", status_code=303)

@app.post("/tarea/clasificar", response_model=Tarea)
async def crear_y_clasificar_tarea(tarea: Tarea):
     # Pasamos el JSON recibido por la infraestructura de la clase POO
     tarea_procesada = matriz.clasificar_tarea(tarea)
     disparar_webhook_n8n(tarea_procesada)
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

@app.put("/tarea/{tarea_id}/editar", response_model=Tarea)
async def editar_tarea_detalle(tarea_id: str, tarea_data: Tarea):
    """Modifica el título, urgencia e importancia de una tarea, recalculando su cuadrante y disparando webhook."""
    from fastapi import HTTPException
    tarea = matriz.editar_tarea(
        tarea_id=tarea_id,
        titulo=tarea_data.titulo,
        urgente=tarea_data.urgente,
        importante=tarea_data.importante
    )
    if not tarea:
        raise HTTPException(status_code=404, detail="Tarea no encontrada")
    disparar_webhook_n8n(tarea)
    return tarea