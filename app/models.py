from pydantic import BaseModel, Field
from typing import List, Dict
import uuid

class Tarea(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
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
        
        # Evitar duplicados si la tarea ya existe en el tablero
        for col in self.tablero_kanban.values():
            for t in col:
                if t.id == tarea.id:
                    return t

        self.tablero_kanban["To Do"].append(tarea)
        return tarea

    def obtener_tarea(self, tarea_id: str) -> Tarea | None:
        """Busca una tarea por su ID en todas las columnas del tablero."""
        for col in self.tablero_kanban.values():
            for tarea in col:
                if tarea.id == tarea_id:
                    return tarea
        return None

    def mover_tarea(self, tarea_id: str, nuevo_estado: str) -> Tarea | None:
        """Mueve una tarea de su columna actual a nuevo_estado si existe y el estado es válido."""
        if nuevo_estado not in self.tablero_kanban:
            return None
        
        tarea = self.obtener_tarea(tarea_id)
        if not tarea:
            return None
        
        # Eliminar de la columna actual
        columna_actual = tarea.estado
        self.tablero_kanban[columna_actual] = [t for t in self.tablero_kanban[columna_actual] if t.id != tarea_id]
        
        # Actualizar estado y agregar a la nueva columna
        tarea.estado = nuevo_estado
        self.tablero_kanban[nuevo_estado].append(tarea)
        return tarea

    def eliminar_tarea(self, tarea_id: str) -> bool:
        """Elimina una tarea del tablero por su ID."""
        tarea = self.obtener_tarea(tarea_id)
        if not tarea:
            return False
        
        columna_actual = tarea.estado
        self.tablero_kanban[columna_actual] = [t for t in self.tablero_kanban[columna_actual] if t.id != tarea_id]
        return True