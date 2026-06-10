from pydantic import BaseModel
from typing import List, Dict

class Tarea(BaseModel):
    id: int
    titulo: str
    urgente: bool
    importante: bool
    estado: str = "To Do"
    cuadrante: str = ""

class MatrizEisenhower:
    def __init__(self):
        self.tablero_kanban: Dict[str, List[Tarea]] = {
            "To Do": [],
            "In Progress": [],
            "Done": []
        }

    def clasificar_tarea(self, tarea: Tarea) -> Tarea:
        if tarea.importante and tarea.urgente:
            tarea.cuadrante = "Hacer (Q1)"
        elif tarea.importante and not tarea.urgente:
            tarea.cuadrante = "Programar (Q2)"
        elif not tarea.importante and tarea.urgente:
            tarea.cuadrante = "Delegar (Q3)"
        else:
            tarea.cuadrante = "Eliminar (Q4)"
        
        self.tablero_kanban["To Do"].append(tarea)
        return tarea