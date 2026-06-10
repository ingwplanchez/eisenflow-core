# main.py
from fastapi import FastAPI
from app.models import Tarea, MatrizEisenhower 

app = FastAPI(
    title="EisenFlow API Core",
    description="API para clasificar tareas según la Matriz de Eisenhower y gestionar un tablero Kanban.",
    version="1.0.0")

matriz = MatrizEisenhower() # Instanciamos el backend en memoria

@app.get("/")
async def root():
    return {"message": "EisenFlow API is running. Go to /docs or /redoc for documentation."}

@app.post("/tarea/clasificar", response_model=Tarea)
async def crear_y_clasificar_tarea(tarea: Tarea):
     # Pasamos el JSON recibido por la infraestructura de la clase POO
     tarea_procesada = matriz.clasificar_tarea(tarea)
     return tarea_procesada

@app.get("/tablero")
async def obtener_tablero():
    return matriz.tablero_kanban